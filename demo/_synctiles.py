#!/usr/bin/env python
#
# _synctiles - Generate and upload Deep Zoom tiles for test slides
#
# Copyright (c) 2010-2015 Carnegie Mellon University
# Copyright (c) 2016 Benjamin Gilbert
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

import boto
from boto.exception import S3ResponseError
from boto.s3.cors import CORSConfiguration
from cStringIO import StringIO
from hashlib import sha256
import json
from multiprocessing import Pool
import openslide
from openslide import OpenSlide, ImageSlide, OpenSlideError
from openslide.deepzoom import DeepZoomGenerator
from optparse import OptionParser
import os
import posixpath as urlpath
import re
import requests
import shutil
import sys
from tempfile import mkdtemp
from unicodedata import normalize
from urlparse import urljoin
from zipfile import ZipFile

STAMP_VERSION = 'size-510'  # change to retile without OpenSlide version bump
# work around https://github.com/boto/boto/issues/2836
S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
S3_BUCKET = 'demo.openslide.org'
BASE_URL = 'http://%s/' % S3_BUCKET
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
    'index.html': {
        'headers': {
            'Content-Type': 'text/html',
            'x-amz-website-redirect-location': 'http://openslide.org/demo/',
        },
    },
    'error.html': {
        'data': '<!doctype html>\n<title>Error</title>\n<h1>Not Found</h1>\nNo such file.\n',
        'headers': {
            'Content-Type': 'text/html',
        },
    },
    'robots.txt': {
        'data': 'User-agent: *\nDisallow: /\n',
        'headers': {
            'Content-Type': 'text/plain',
        },
    },
}
HEADERS_NOCACHE = {
    'Cache-Control': 'no-cache',
}
HEADERS_CACHE = {
    'Cache-Control': 'public, max-age=31536000',
}


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
            for name, image in slide.associated_images.iteritems():
                self._generators[name] = generator(ImageSlide(image))
        return self._generators[associated]


def connect_bucket():
    conn = boto.connect_s3(calling_format=S3_CALLING_FORMAT)
    return conn.get_bucket(S3_BUCKET)


def pool_init():
    global generator_cache, upload_bucket
    generator_cache = GeneratorCache()
    upload_bucket = connect_bucket()


def sync_tile(args):
    """Generate and possibly upload a tile."""
    try:
        slide_path, associated, level, address, key_name, cur_md5 = args
        dz = generator_cache.get_dz(slide_path, associated)
        tile = dz.get_tile(level, address)
        buf = StringIO()
        tile.save(buf, FORMAT, quality=QUALITY)
        buf.seek(0)
        key = upload_bucket.new_key(key_name)
        md5_hex, md5_b64 = key.compute_md5(buf)
        if cur_md5 != md5_hex:
            key.content_type = 'image/%s' % FORMAT
            key.set_contents_from_file(buf, md5=(md5_hex, md5_b64),
                        policy='public-read', headers=HEADERS_CACHE)
        return key_name
    except BaseException, e:
        return e


def enumerate_tiles(slide_path, associated, dz, key_imagepath, key_md5sums):
    """Enumerate tiles in a single image."""
    for level in xrange(dz.level_count):
        key_levelpath = urlpath.join(key_imagepath, str(level))
        cols, rows = dz.level_tiles[level]
        for row in xrange(rows):
            for col in xrange(cols):
                key_name = urlpath.join(key_levelpath, '%d_%d.%s' % (
                                col, row, FORMAT))
                yield (slide_path, associated, level, (col, row), key_name,
                        key_md5sums.get(key_name))


def sync_image(pool, slide_relpath, slide_path, associated, dz, key_basepath,
        key_md5sums, mpp=None):
    """Generate and upload tiles, and generate metadata, for a single image.
    Delete valid tiles from key_md5sums."""

    count = 0
    total = dz.tile_count
    associated_slug = slugify(associated) if associated else VIEWER_SLIDE_NAME
    key_imagepath = urlpath.join(key_basepath, '%s_files' % associated_slug)
    iterator = enumerate_tiles(slide_path, associated, dz, key_imagepath,
            key_md5sums)

    def progress():
        print "Tiling %s %s: %d/%d tiles\r" % (slide_relpath,
                associated_slug, count, total),
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
    print

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
    key = bucket.new_key(path)
    key.content_type = 'application/json'
    buf = json.dumps(item, indent=1, sort_keys=True)
    key.set_contents_from_string(buf, policy='public-read',
            headers=HEADERS_CACHE if cache else HEADERS_NOCACHE)


def sync_slide(stamp, pool, bucket, slide_relpath, slide_info):
    """Generate and upload tiles and metadata for a single slide."""

    key_basepath = urlpath.splitext(slide_relpath)[0].lower()
    metadata_key_name = urlpath.join(key_basepath, SLIDE_METADATA_NAME)
    properties_key_name = urlpath.join(key_basepath, SLIDE_PROPERTIES_NAME)

    # Get current metadata
    try:
        metadata = bucket.new_key(metadata_key_name).get_contents_as_string()
        metadata = json.loads(metadata)
    except S3ResponseError, e:
        if e.status == 404:
            metadata = None
        else:
            raise

    # Return if metadata is current
    if metadata is not None and metadata['stamp'] == stamp:
        return metadata

    tempdir = mkdtemp(prefix='synctiles-', dir='/var/tmp')
    try:
        # Fetch slide
        print 'Fetching %s...' % slide_relpath
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
            raise IOError('Short read fetching %s' % slide_relpath)
        if hash.hexdigest() != slide_info['sha256']:
            raise IOError('Hash mismatch fetching %s' % slide_relpath)

        # Open slide
        slide = None
        try:
            slide = OpenSlide(slide_path)
        except OpenSlideError:
            if urlpath.splitext(slide_relpath)[1] == '.zip':
                # Unzip slide
                print 'Extracting %s...' % slide_relpath
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
        print "Enumerating keys for %s..." % slide_relpath
        key_md5sums = {}
        for key in bucket.list(prefix=key_basepath + '/'):
            key_md5sums[key.name] = key.etag.strip('"')

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
        print "Pruning %d keys for %s..." % (len(key_md5sums), slide_relpath)
        delete_result = bucket.delete_keys(key_md5sums, quiet=True)
        if delete_result.errors:
            raise IOError('Failed to delete %d keys' %
                    len(delete_result.errors))

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
        'stamp': sha256('%s %s %s' % (openslide.__library_version__,
                openslide.__version__, STAMP_VERSION)).hexdigest()[:8],
        'groups': [],
    }
    print 'OpenSlide %(openslide)s, OpenSlide Python %(openslide_python)s' % metadata

    # Get openslide-testdata index
    r = requests.get(urljoin(DOWNLOAD_BASE_URL, DOWNLOAD_INDEX))
    r.raise_for_status()
    slides = r.json()

    # Connect to S3
    bucket = connect_bucket()

    # Set bucket configuration
    print "Configuring bucket..."
    cors = CORSConfiguration()
    cors.add_rule(['GET'], CORS_ORIGINS)
    bucket.set_cors(cors)

    # Store static files
    print "Storing static files..."
    for relpath, opts in BUCKET_STATIC.iteritems():
        key = bucket.new_key(relpath)
        key.set_contents_from_string(opts.get('data', ''),
                headers=opts.get('headers', {}), policy='public-read')

    # If the stamp is changing, mark bucket dirty
    try:
        old_stamp = json.loads(bucket.new_key(METADATA_NAME).
                get_contents_as_string()).get('stamp')
    except S3ResponseError, e:
        if e.status == 404:
            old_stamp = None
        else:
            raise
    if metadata['stamp'] != old_stamp:
        print 'Marking bucket dirty...'
        upload_status(bucket, dirty=True, stamp=old_stamp)

    # Tile and upload slides
    cur_group_name = None
    cur_slides = None
    pool = Pool(workers, pool_init)
    try:
        for slide_relpath, slide_info in sorted(slides.items()):
            slide = sync_slide(metadata['stamp'], pool, bucket, slide_relpath,
                    slide_info)
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
    print 'Storing metadata...'
    upload_metadata(bucket, METADATA_NAME, metadata, False)

    # Mark bucket clean
    print 'Marking bucket clean...'
    upload_status(bucket, stamp=metadata['stamp'])


if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog [options]')
    parser.add_option('-j', '--jobs', metavar='COUNT', dest='workers',
                type='int', default=4,
                help='number of worker processes to start [4]')

    (opts, args) = parser.parse_args()
    if args:
        parser.error('Too many arguments')

    sync_slides(opts.workers)
