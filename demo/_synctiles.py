#!/usr/bin/env python3
#
# _synctiles - Generate and upload Deep Zoom tiles for test slides
#
# Copyright (c) 2010-2015 Carnegie Mellon University
# Copyright (c) 2016-2023 Benjamin Gilbert
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
from PIL import ImageCms
import posixpath as urlpath
import re
import requests
import shutil
import sys
from tempfile import mkdtemp
from unicodedata import normalize
from urllib.parse import urljoin
from zipfile import ZipFile
import zlib

STAMP_VERSION = 'size-510'  # change to retile without OpenSlide version bump
S3_BUCKET = 'openslide-demo'
S3_REGION = 'us-east-1'
BASE_URL = f'https://{S3_BUCKET}.s3.dualstack.{S3_REGION}.amazonaws.com/'
CORS_ORIGINS = ['*']
DOWNLOAD_BASE_URL = 'https://openslide.cs.cmu.edu/download/openslide-testdata/'
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
RENDERING_INTENT = ImageCms.Intent.ABSOLUTE_COLORIMETRIC
GROUP_NAME_MAP = {
    'Generic-TIFF': 'Generic TIFF',
    'Hamamatsu': 'Hamamatsu NDPI',
    'Hamamatsu-vms': 'Hamamatsu VMS',
    'Mirax': 'MIRAX',
    'Philips-TIFF': 'Philips TIFF',
}
BUCKET_STATIC = {
    'robots.txt': {
        'data': 'User-agent: *\nDisallow: /\n',
        'content-type': 'text/plain',
    },
}
CACHE_CONTROL_NOCACHE = 'no-cache'
CACHE_CONTROL_CACHE = 'public, max-age=31536000'

# Optimized sRGB v2 profile, CC0-1.0 license
# https://github.com/saucecontrol/Compact-ICC-Profiles/blob/bdd84663/profiles/sRGB-v2-micro.icc
# ImageCms.createProfile() generates a v4 profile and Firefox has problems
# with those: https://littlecms.com/blog/2020/09/09/browser-check/
SRGB_PROFILE_BYTES = zlib.decompress(
    base64.b64decode(
        'eNpjYGA8kZOcW8wkwMCQm1dSFOTupBARGaXA/oiBmUGEgZOBj0E2Mbm4wDfYLYQBCIoT'
        'y4uTS4pyGFDAt2sMjCD6sm5GYl7K3IkMtg4NG2wdSnQa5y1V6mPADzhTUouTgfQHII5P'
        'LigqYWBg5AGyecpLCkBsCSBbpAjoKCBbB8ROh7AdQOwkCDsErCYkyBnIzgCyE9KR2ElI'
        'bKhdIMBaCvQsskNKUitKQLSzswEDKAwgop9DwH5jFDuJEMtfwMBg8YmBgbkfIZY0jYFh'
        'eycDg8QthJgKUB1/KwPDtiPJpUVlUGu0gLiG4QfjHKZS5maWk2x+HEJcEjxJfF8Ez4t8'
        'k8iS0VNwVlmjmaVXZ/zacrP9NbdwX7OQshjxFNmcttKwut4OnUlmc1Yv79l0e9/MU8ev'
        'pz4p//jz/38AR4Nk5Q=='
    )
)
SRGB_PROFILE = ImageCms.getOpenProfile(BytesIO(SRGB_PROFILE_BYTES))

def slugify(text):
    """Generate an ASCII-only slug."""
    text = normalize('NFKD', text.lower()).encode('ascii', 'ignore').decode()
    return re.sub('[^a-z0-9]+', '_', text)


def get_transform(image):
    """Return a function that transforms an image to sRGB in place."""
    if image.color_profile is None:
        return lambda img: None
    transform = ImageCms.buildTransform(
        image.color_profile, SRGB_PROFILE, 'RGB', 'RGB', RENDERING_INTENT, 0
    )
    def xfrm(img):
        ImageCms.applyTransform(img, transform, True)
        # Some browsers assume we intend the display's color space if we
        # don't embed the profile.  Pillow's serialization is larger, so
        # use ours.
        img.info['icc_profile'] = SRGB_PROFILE_BYTES
    return xfrm


def connect_bucket():
    conn = boto3.resource('s3')
    return conn, conn.Bucket(S3_BUCKET)


def pool_init(slide_path):
    global upload_bucket, dz_generators
    _, upload_bucket = connect_bucket()
    generator = lambda slide: (
        DeepZoomGenerator(slide, TILE_SIZE, OVERLAP, limit_bounds=LIMIT_BOUNDS),
        get_transform(slide)
    )
    slide = OpenSlide(slide_path)
    dz_generators = {
        None: generator(slide)
    }
    for name, image in slide.associated_images.items():
        dz_generators[name] = generator(ImageSlide(image))


def sync_tile(args):
    """Generate and possibly upload a tile."""
    try:
        associated, level, address, key_name, cur_md5 = args
        dz, transform = dz_generators[associated]
        tile = dz.get_tile(level, address)
        transform(tile)
        buf = BytesIO()
        tile.save(buf, FORMAT, quality=QUALITY,
                icc_profile=tile.info.get('icc_profile'))
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


def enumerate_tiles(associated, dz, key_imagepath, key_md5sums):
    """Enumerate tiles in a single image."""
    for level in range(dz.level_count):
        key_levelpath = urlpath.join(key_imagepath, str(level))
        cols, rows = dz.level_tiles[level]
        for row in range(rows):
            for col in range(cols):
                key_name = urlpath.join(key_levelpath, f'{col}_{row}.{FORMAT}')
                yield (associated, level, (col, row), key_name,
                        key_md5sums.get(key_name))


def sync_image(pool, slide_relpath, associated, dz, key_basepath, key_md5sums,
        mpp=None):
    """Generate and upload tiles, and generate metadata, for a single image.
    Delete valid tiles from key_md5sums."""

    count = 0
    total = dz.tile_count
    associated_slug = slugify(associated) if associated else VIEWER_SLIDE_NAME
    key_imagepath = urlpath.join(key_basepath, f'{associated_slug}_files')
    iterator = enumerate_tiles(associated, dz, key_imagepath, key_md5sums)

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


def sync_slide(stamp, conn, bucket, slide_relpath, slide_info, workers):
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

            # Start compute pool
            pool = Pool(workers, lambda: pool_init(slide_path))
            try:
                # Tile slide
                def do_tile(associated, image):
                    dz = DeepZoomGenerator(image, TILE_SIZE, OVERLAP,
                                limit_bounds=LIMIT_BOUNDS)
                    return sync_image(pool, slide_relpath, associated, dz,
                            key_basepath, key_md5sums,
                            mpp if associated is None else None)
                metadata['slide'] = do_tile(None, slide)

                # Tile associated images
                for associated, image in sorted(slide.associated_images.items()):
                    cur_props = do_tile(associated, ImageSlide(image))
                    metadata['associated'].append(cur_props)
            except:
                pool.terminate()
                raise
            finally:
                pool.close()
                pool.join()
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


def start_retile(ctxfile, matrixfile):
    """Subcommand to initialize a retiling run.  Writes common state into
    ctxfile and a list of slides to be retiled into matrixfile."""

    # Get openslide-testdata index
    r = requests.get(urljoin(DOWNLOAD_BASE_URL, DOWNLOAD_INDEX))
    r.raise_for_status()
    slides = r.json()

    # Initialize context for the run
    context = {
        'openslide': openslide.__library_version__,
        'openslide_python': openslide.__version__,
        'stamp': sha256(f'{openslide.__library_version__} {openslide.__version__} {STAMP_VERSION}'.encode()) \
                .hexdigest()[:8],
        'slides': slides,
    }
    print(f'OpenSlide {context["openslide"]}, OpenSlide Python {context["openslide_python"]}')

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
    if context['stamp'] != old_stamp:
        print('Marking bucket dirty...')
        upload_status(bucket, dirty=True, stamp=old_stamp)

    # Write output files
    with open(ctxfile, 'w') as fh:
        json.dump(context, fh)
    with open(matrixfile, 'w') as fh:
        json.dump({
            "slide": sorted(slides.keys()),
        }, fh)


def retile_slide(ctxfile, slide_relpath, summarydir, workers):
    """Subcommand to retile one slide into S3.  Writes summary data into
    summarydir."""

    # Load context
    with open(ctxfile) as fh:
        context = json.load(fh)

    # Connect to S3
    conn, bucket = connect_bucket()

    # Tile slide
    slide_info = context['slides'].get(slide_relpath)
    if slide_info is None:
        raise Exception(f'No such slide {slide_relpath}')
    summary = sync_slide(context['stamp'], conn, bucket, slide_relpath,
            slide_info, workers)

    # Write summary if the slide was readable
    if 'slide' in summary:
        summary.pop('properties', None)
        summary.pop('stamp', None)
        summary.update({
            'credit': slide_info.get('credit'),
            'description': slide_info['description'],
            'download_url': urljoin(DOWNLOAD_BASE_URL, slide_relpath),
        })
        summaryfile = os.path.join(summarydir, slide_relpath)
        os.makedirs(os.path.dirname(summaryfile), exist_ok=True)
        with open(summaryfile, 'w') as fh:
            json.dump(summary, fh)


def finish_retile(ctxfile, summarydir):
    """Subcommand to finish a retiling run.  Reads context file and summary
    dir and writes metadata to S3."""

    # Load context
    with open(ctxfile) as fh:
        context = json.load(fh)

    # Connect to S3
    conn, bucket = connect_bucket()

    # Build group list
    groups = []
    cur_group_name = None
    cur_slides = None
    for slide_relpath, slide_info in sorted(context['slides'].items()):
        summaryfile = os.path.join(summarydir, slide_relpath)
        if os.path.exists(summaryfile):
            with open(summaryfile) as fh:
                summary = json.load(fh)
            group_name = urlpath.dirname(slide_relpath)
            if group_name != cur_group_name:
                cur_group_name = group_name
                cur_slides = []
                groups.append({
                    'name': GROUP_NAME_MAP.get(group_name, group_name),
                    'slides': cur_slides
                })
            cur_slides.append(summary)

    # Upload metadata
    print('Storing metadata...')
    metadata = {
        'openslide': context['openslide'],
        'openslide_python': context['openslide_python'],
        'stamp': context['stamp'],
        'groups': groups,
    }
    upload_metadata(bucket, METADATA_NAME, metadata, False)

    # Mark bucket clean
    print('Marking bucket clean...')
    upload_status(bucket, stamp=context['stamp'])


if __name__ == '__main__':
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(metavar='subcommand', required=True)

    parser_start = subparsers.add_parser('start',
            help='start a retiling run')
    parser_start.add_argument('context_file',
            help='path to context file (output)')
    parser_start.add_argument('matrix_file',
            help='path to list of slides to tile (output)')
    parser_start.set_defaults(cmd='start')

    parser_tile = subparsers.add_parser('tile',
            help='retile one slide')
    parser_tile.add_argument('context_file',
            help='path to context file')
    parser_tile.add_argument('slide',
            help='slide identifier (from matrix file)')
    parser_tile.add_argument('summary_dir',
            help='path to summary directory (output)')
    parser_tile.add_argument('-j', '--jobs', metavar='COUNT', dest='workers',
                type=int, default=4,
                help='number of worker processes to start [4]')
    parser_tile.set_defaults(cmd='tile')

    parser_finish = subparsers.add_parser('finish',
            help='finish a retiling run')
    parser_finish.add_argument('context_file',
            help='path to context file')
    parser_finish.add_argument('summary_dir',
            help='path to summary directory')
    parser_finish.set_defaults(cmd='finish')

    args = parser.parse_args()
    if args.cmd == 'start':
        start_retile(args.context_file, args.matrix_file)
    elif args.cmd == 'tile':
        retile_slide(args.context_file, args.slide, args.summary_dir,
                args.workers)
    elif args.cmd == 'finish':
        finish_retile(args.context_file, args.summary_dir)
    else:
        raise Exception('unimplemented subcommand')
