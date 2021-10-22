#!/usr/bin/env python3
#
# _synctiles - Generate and upload Deep Zoom tiles for test slides
#
# Copyright (c) 2010-2015 Carnegie Mellon University
# Copyright (c) 2016-2021 Benjamin Gilbert
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of version 2.1 of the GNU Lesser General Public License
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from argparse import ArgumentParser
import base64
import boto3
from hashlib import md5, sha256
from io import BytesIO
import json
from multiprocessing import Pool
import openslide
from openslide import OpenSlide, ImageSlide, OpenSlideError
from openslide.deepzoom import DeepZoomGenerator
import os
import posixpath as urlpath
import re
import requests
import shutil
import sys
from tempfile import mkdtemp
from unicodedata import normalize
from urllib.parse import urljoin
from zipfile import ZipFile

STAMP_VERSION = 'size-510'  # change to retile without OpenSlide version bump
S3_BUCKET = 'openslide-demo'
S3_REGION = 'us-east-1'
BASE_URL = f'https://{S3_BUCKET}.s3.dualstack.{S3_REGION}.amazonaws.com/'
CORS_ORIGINS = ['*']
DOWNLOAD_BASE_URL = 'http://openslide.cs.cmu.edu/download/openslide-testdata/'
DOWNLOAD_INDEX = 'index.json'
VIEWER_SLIDE_NAME = 'slide'
METADATA_NAME = 'info.json'
STATUS_NAME = 'status.json'
SLIDE_PROPERTIES_NAME = 'properties.json'
SLIDE_METADATA_NAME = 'slide.json'
FORMAT = 'jpeg'
QUALITY = 75
TILE_SIZE = 510
OVERLAP = 1
LIMIT_BOUNDS = True
GROUP_NAME_MAP = {
    'Generic-TIFF': 'Generic TIFF',
    'Hamamatsu': 'Hamamatsu NDPI',
    'Hamamatsu-vms': 'Hamamatsu VMS',
    'Mirax': 'MIRAX',
}
BUCKET_STATIC = {
    'robots.txt': {
        'data': 'User-agent: *\nDisallow: /\n',
        'content-type': 'text/plain',
    },
}
CACHE_CONTROL_NOCACHE = 'no-cache'
CACHE_CONTROL_CACHE = 'public, max-age=31536000'


def slugify(text):
    """Generate an ASCII-only slug."""
    text = normalize('NFKD', text.lower()).encode('ascii', 'ignore').decode()
    return re.sub('[^a-z0-9]+', '_', text)


class GeneratorCache(object):
    def __init__(self):
        self._slide_path = ''
        self._generators = {}

    def get_dz(self, slide_path, associated=None):
        if slide_path != self._slide_path:
            generator = lambda slide: DeepZoomGenerator(slide, TILE_SIZE,
                        OVERLAP, limit_bounds=LIMIT_BOUNDS)
            slide = OpenSlide(slide_path)
            self._slide_path = slide_path
            self._generators = {
                None: generator(slide)
            }
            for name, image in slide.associated_images.items():
                self._generators[name] = generator(ImageSlide(image))
        return self._generators[associated]


def connect_bucket():
    conn = boto3.resource('s3')
    return conn, conn.Bucket(S3_BUCKET)


def pool_init():
    global generator_cache, upload_bucket
    generator_cache = GeneratorCache()
    _, upload_bucket = connect_bucket()


def sync_tile(args):
    """Generate and possibly upload a tile."""
    try:
        slide_path, associated, level, address, key_name, cur_md5 = args
        dz = generator_cache.get_dz(slide_path, associated)
        tile = dz.get_tile(level, address)
        buf = BytesIO()
        tile.save(buf, FORMAT, quality=QUALITY)
        new_md5 = md5(buf.getbuffer())
        if cur_md5 != new_md5.hexdigest():
            upload_bucket.Object(key_name).put(
                ACL='public-read',
                Body=buf.getvalue(),
                CacheControl=CACHE_CONTROL_CACHE,
                ContentMD5=base64.b64encode(new_md5.digest()).decode(),
                ContentType=f'image/{FORMAT}',
            )
        return key_name
    except BaseException as e:
        return e


def enumerate_tiles(slide_path, associated, dz, key_imagepath, key_md5sums):
    """Enumerate tiles in a single image."""
    for level in range(dz.level_count):
        key_levelpath = urlpath.join(key_imagepath, str(level))
        cols, rows = dz.level_tiles[level]
        for row in range(rows):
            for col in range(cols):
                key_name = urlpath.join(key_levelpath, f'{col}_{row}.{FORMAT}')
                yield (slide_path, associated, level, (col, row), key_name,
                        key_md5sums.get(key_name))


def sync_image(pool, slide_relpath, slide_path, associated, dz, key_basepath,
        key_md5sums, mpp=None):
    """Generate and upload tiles, and generate metadata, for a single image.
    Delete valid tiles from key_md5sums."""

    count = 0
    total = dz.tile_count
    associated_slug = slugify(associated) if associated else VIEWER_SLIDE_NAME
    key_imagepath = urlpath.join(key_basepath, f'{associated_slug}_files')
    iterator = enumerate_tiles(slide_path, associated, dz, key_imagepath,
            key_md5sums)

    def progress():
        print(f"Tiling {slide_relpath} {associated_slug}: {count}/{total} tiles\r",
                end='')
        sys.stdout.flush()

    # Sync tiles
    progress()
    for ret in pool.imap_unordered(sync_tile, iterator, 32):
        if isinstance(ret, BaseException):
            raise ret
        else:
            key_md5sums.pop(ret, None)
        count += 1
        if count % 100 == 0:
            progress()
    progress()
    print()

    # Format tile source
    source = {
        'Image': {
            'xmlns': 'http://schemas.microsoft.com/deepzoom/2008',
            'Url': urljoin(BASE_URL, key_imagepath) + '/',
            'Format': FORMAT,
            'TileSize': TILE_SIZE,
            'Overlap': OVERLAP,
            'Size': {
                'Width': dz.level_dimensions[-1][0],
                'Height': dz.level_dimensions[-1][1],
            },
        }
    }

    # Return metadata
    return {
        'name': associated,
        'mpp': mpp,
        'source': source,
    }


def upload_metadata(bucket, path, item, cache=True):
    bucket.Object(path).put(
        ACL='public-read',
        Body=json.dumps(item, indent=1, sort_keys=True).encode(),
        CacheControl=CACHE_CONTROL_CACHE if cache else CACHE_CONTROL_NOCACHE,
        ContentType='application/json',
    )


def sync_slide(stamp, pool, conn, bucket, slide_relpath, slide_info):
    """Generate and upload tiles and metadata for a single slide."""

    key_basepath = urlpath.splitext(slide_relpath)[0].lower()
    metadata_key_name = urlpath.join(key_basepath, SLIDE_METADATA_NAME)
    properties_key_name = urlpath.join(key_basepath, SLIDE_PROPERTIES_NAME)

    # Get current metadata
    try:
        metadata = json.load(bucket.Object(metadata_key_name).get()['Body'])
    except conn.meta.client.exceptions.NoSuchKey:
        metadata = None

    # Return if metadata is current
    if metadata is not None and metadata['stamp'] == stamp:
        return metadata

    tempdir = mkdtemp(prefix='synctiles-', dir='/var/tmp')
    try:
        # Fetch slide
        print(f'Fetching {slide_relpath}...')
        count = 0
        hash = sha256()
        slide_path = os.path.join(tempdir, urlpath.basename(slide_relpath))
        with open(slide_path, 'wb') as fh:
            r = requests.get(urljoin(DOWNLOAD_BASE_URL, slide_relpath),
                    stream=True)
            r.raise_for_status()
            for buf in r.iter_content(10 << 20):
                if not buf:
                    break
                fh.write(buf)
                hash.update(buf)
                count += len(buf)
        if count != int(r.headers['Content-Length']):
            raise IOError(f'Short read fetching {slide_relpath}')
        if hash.hexdigest() != slide_info['sha256']:
            raise IOError(f'Hash mismatch fetching {slide_relpath}')

        # Open slide
        slide = None
        try:
            slide = OpenSlide(slide_path)
        except OpenSlideError:
            if urlpath.splitext(slide_relpath)[1] == '.zip':
                # Unzip slide
                print(f'Extracting {slide_relpath}...')
                temp_path = mkdtemp(dir=tempdir)
                with ZipFile(slide_path) as zf:
                    zf.extractall(path=temp_path)
                # Find slide in zip
                for sub_name in os.listdir(temp_path):
                    try:
                        slide_path = os.path.join(temp_path, sub_name)
                        slide = OpenSlide(slide_path)
                    except OpenSlideError:
                        pass
                    else:
                        break
        # slide will be None if we can't read it

        # Enumerate existing keys
        print(f"Enumerating keys for {slide_relpath}...")
        key_md5sums = {}
        for obj in bucket.objects.filter(Prefix=key_basepath + '/'):
            key_md5sums[obj.key] = obj.e_tag.strip('"')

        # Initialize metadata
        metadata = {
            'name': urlpath.splitext(urlpath.basename(slide_relpath))[0],
            'stamp': stamp,
        }

        if slide is not None:
            # Add slide metadata
            metadata.update({
                'associated': [],
                'properties': dict(slide.properties),
                'properties_url': urljoin(BASE_URL, properties_key_name) +
                        '?v=' + stamp,
            })

            # Calculate microns per pixel
            try:
                mpp_x = slide.properties[openslide.PROPERTY_NAME_MPP_X]
                mpp_y = slide.properties[openslide.PROPERTY_NAME_MPP_Y]
                mpp = (float(mpp_x) + float(mpp_y)) / 2
            except (KeyError, ValueError):
                mpp = None

            # Tile slide
            def do_tile(associated, image):
                dz = DeepZoomGenerator(image, TILE_SIZE, OVERLAP,
                            limit_bounds=LIMIT_BOUNDS)
                return sync_image(pool, slide_relpath, slide_path,
                        associated, dz, key_basepath, key_md5sums,
                        mpp if associated is None else None)
            metadata['slide'] = do_tile(None, slide)

            # Tile associated images
            for associated, image in sorted(slide.associated_images.items()):
                cur_props = do_tile(associated, ImageSlide(image))
                metadata['associated'].append(cur_props)
    finally:
        shutil.rmtree(tempdir)

    # Delete old keys
    for name in metadata_key_name, properties_key_name:
        key_md5sums.pop(name, None)
    if key_md5sums:
        to_delete = [k for k in key_md5sums]
        print(f"Pruning {len(to_delete)} keys for {slide_relpath}...")
        while to_delete:
            cur_delete, to_delete = to_delete[0:1000], to_delete[1000:]
            delete_result = bucket.delete_objects(
                Delete={
                    'Objects': [{'Key': k} for k in cur_delete],
                    'Quiet': True,
                },
            )
            if 'Errors' in delete_result:
                raise IOError(f'Failed to delete {len(delete_result["Errors"])} keys')

    # Update metadata
    if 'properties' in metadata:
        upload_metadata(bucket, properties_key_name, metadata['properties'])
    upload_metadata(bucket, metadata_key_name, metadata, cache=False)

    return metadata


def upload_status(bucket, dirty=False, stamp=None):
    status = {
        'dirty': dirty,
        'stamp': stamp,
    }
    upload_metadata(bucket, STATUS_NAME, status, False)


def sync_slides(workers):
    """Tile openslide-testdata and synchronize into S3."""

    # Initialize metadata
    metadata = {
        'openslide': openslide.__library_version__,
        'openslide_python': openslide.__version__,
        'stamp': sha256(f'{openslide.__library_version__} {openslide.__version__} {STAMP_VERSION}'.encode()) \
                .hexdigest()[:8],
        'groups': [],
    }
    print(f'OpenSlide {metadata["openslide"]}, OpenSlide Python {metadata["openslide_python"]}')

    # Get openslide-testdata index
    r = requests.get(urljoin(DOWNLOAD_BASE_URL, DOWNLOAD_INDEX))
    r.raise_for_status()
    slides = r.json()

    # Connect to S3
    conn, bucket = connect_bucket()

    # Set bucket configuration
    print("Configuring bucket...")
    bucket.Cors().put(
        CORSConfiguration={
            'CORSRules': [
                {
                    'AllowedMethods': ['GET'],
                    'AllowedOrigins': CORS_ORIGINS,
                },
            ],
        }
    )

    # Store static files
    print("Storing static files...")
    for relpath, opts in BUCKET_STATIC.items():
        bucket.Object(relpath).put(
            ACL='public-read',
            Body=opts.get('data', '').encode(),
            ContentType=opts.get('content-type'),
        )

    # If the stamp is changing, mark bucket dirty
    try:
        stream = bucket.Object(METADATA_NAME).get()['Body']
        old_stamp = json.load(stream).get('stamp')
    except conn.meta.client.exceptions.NoSuchKey:
        old_stamp = None
    if metadata['stamp'] != old_stamp:
        print('Marking bucket dirty...')
        upload_status(bucket, dirty=True, stamp=old_stamp)

    # Tile and upload slides
    cur_group_name = None
    cur_slides = None
    pool = Pool(workers, pool_init)
    try:
        for slide_relpath, slide_info in sorted(slides.items()):
            slide = sync_slide(metadata['stamp'], pool, conn, bucket,
                    slide_relpath, slide_info)
            # Skip unreadable slides
            if 'slide' in slide:
                group_name = urlpath.dirname(slide_relpath)
                if group_name != cur_group_name:
                    cur_group_name = group_name
                    cur_slides = []
                    metadata['groups'].append({
                        'name': GROUP_NAME_MAP.get(group_name, group_name),
                        'slides': cur_slides
                    })
                # Rearrange slide-level metadata for top-level metadata
                slide.pop('properties', None)
                slide.pop('stamp', None)
                slide.update({
                    'credit': slide_info.get('credit'),
                    'description': slide_info['description'],
                    'download_url': urljoin(DOWNLOAD_BASE_URL, slide_relpath),
                })
                cur_slides.append(slide)
    except:
        pool.terminate()
        raise
    finally:
        pool.close()
        pool.join()

    # Upload metadata
    print('Storing metadata...')
    upload_metadata(bucket, METADATA_NAME, metadata, False)

    # Mark bucket clean
    print('Marking bucket clean...')
    upload_status(bucket, stamp=metadata['stamp'])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-j', '--jobs', metavar='COUNT', dest='workers',
                type=int, default=4,
                help='number of worker processes to start [4]')

    args = parser.parse_args()
    sync_slides(args.workers)
