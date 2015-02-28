#!/usr/bin/env python
#
# _synctiles - Generate and upload Deep Zoom tiles for test slides
#
# Copyright (c) 2010-2014 Carnegie Mellon University
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
from hashlib import sha256
import json
from multiprocessing import Pool
import openslide
from openslide import OpenSlide, ImageSlide, OpenSlideError
from openslide.deepzoom import DeepZoomGenerator
from optparse import OptionParser
import os
import re
import shutil
import sys
from tempfile import mkdtemp
from unicodedata import normalize
import zipfile

STAMP_VERSION = 'initial'  # change to retile without OpenSlide version bump
S3_BUCKET = 'demo.openslide.org'
BASE_URL = 'http://%s/' % S3_BUCKET
DOWNLOAD_BASE_URL = 'http://openslide.cs.cmu.edu/download/openslide-testdata/'
VIEWER_SLIDE_NAME = 'slide'
METADATA_NAME = 'info.js'
SLIDE_PROPERTIES_NAME = 'properties.js'
SLIDE_METADATA_NAME = 'slide.json'
FORMAT = 'jpeg'
QUALITY = 75
TILE_SIZE = 512
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
METADATA_HEADERS = {
    'Cache-Control': 'no-cache',
}
TILE_HEADERS = {
    'Cache-Control': 'public, max-age=31536000',
}


def slugify(text):
    """Generate an ASCII-only slug."""
    text = normalize('NFKD', text.lower()).encode('ascii', 'ignore').decode()
    return re.sub('[^a-z0-9]+', '_', text)


class GeneratorCache(object):
    def __init__(self):
        self._in_path = ''
        self._generators = {}

    def get_dz(self, in_path, associated=None):
        if in_path != self._in_path:
            generator = lambda slide: DeepZoomGenerator(slide, TILE_SIZE,
                        OVERLAP, limit_bounds=LIMIT_BOUNDS)
            slide = OpenSlide(in_path)
            self._in_path = in_path
            self._generators = {
                None: generator(slide)
            }
            for name, image in slide.associated_images.iteritems():
                self._generators[name] = generator(ImageSlide(image))
        return self._generators[associated]


def generate_pool_init():
    global generator_cache
    generator_cache = GeneratorCache()


def process_tile(args):
    """Generate and save a tile."""
    try:
        in_path, associated, level, address, out_path = args
        if not os.path.exists(out_path):
            dz = generator_cache.get_dz(in_path, associated)
            tile = dz.get_tile(level, address)
            tile.save(out_path, quality=QUALITY)
    except KeyboardInterrupt:
        return KeyboardInterrupt


def enumerate_tiles(in_path, associated, dz, out_root, out_relpath):
    """Enumerate tiles in a single image."""
    for level in xrange(dz.level_count):
        dir_path = os.path.join(out_root, "%s_files" % out_relpath, str(level))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        cols, rows = dz.level_tiles[level]
        for row in xrange(rows):
            for col in xrange(cols):
                file_path = os.path.join(dir_path, '%d_%d.%s' % (
                                col, row, FORMAT))
                yield (in_path, associated, level, (col, row), file_path)


def tile_image(pool, in_path, associated, dz, out_root, out_relpath):
    """Generate tiles and metadata for a single image."""

    count = 0
    total = dz.tile_count
    iterator = enumerate_tiles(in_path, associated, dz, out_root, out_relpath)

    def progress():
        print >> sys.stderr, "Tiling %s: wrote %d/%d tiles\r" % (
                    out_relpath, count, total),

    # Write tiles
    progress()
    for ret in pool.imap_unordered(process_tile, iterator, 32):
        count += 1
        if count % 100 == 0:
            progress()
    progress()
    print

    # Format tile source
    source = {
        'Image': {
            'xmlns': 'http://schemas.microsoft.com/deepzoom/2008',
            'Url': os.path.join(BASE_URL, out_relpath + '_files/'),
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
        'source': source,
    }


def tile_slide(pool, in_relpath, in_phys_path, out_name, out_root,
            out_relpath, stamp):
    """Generate tiles and metadata for all images in a slide."""
    try:
        slide = OpenSlide(in_phys_path)
    except OpenSlideError:
        return None
    def do_tile(associated, image, out_relpath):
        dz = DeepZoomGenerator(image, TILE_SIZE, OVERLAP,
                    limit_bounds=LIMIT_BOUNDS)
        return tile_image(pool, in_phys_path, associated, dz, out_root,
                    out_relpath)
    metadata = {
        'name': out_name,
        'stamp': stamp,
        'slide': do_tile(None, slide,
                    os.path.join(out_relpath, VIEWER_SLIDE_NAME)),
        'associated': [],
        'properties': dict(slide.properties),
        'properties_url': os.path.join(BASE_URL, out_relpath,
                    SLIDE_PROPERTIES_NAME) + '?v=' + stamp,
        'download_url': os.path.join(DOWNLOAD_BASE_URL, in_relpath),
    }
    for associated, image in sorted(slide.associated_images.items()):
        cur_props = do_tile(associated, ImageSlide(image),
                    os.path.join(out_relpath, slugify(associated)))
        metadata['associated'].append(cur_props)
    with open(os.path.join(out_root, out_relpath, SLIDE_METADATA_NAME),
                'w') as fh:
        json.dump(metadata, fh, indent=1, sort_keys=True)
    with open(os.path.join(out_root, out_relpath, SLIDE_PROPERTIES_NAME),
                'w') as fh:
        buf = json.dumps(metadata['properties'], indent=1, sort_keys=True)
        fh.write('set_slide_properties(%s);\n' % buf)
    del metadata['properties']
    return metadata


def walk_slides(pool, tempdir, in_root, in_relpath, out_root, out_relpath,
            stamp):
    """Build a directory of tiled images from a directory of slides."""
    slides = []
    for in_name in sorted(os.listdir(os.path.join(in_root, in_relpath))):
        in_cur_relpath = os.path.join(in_relpath, in_name)
        in_cur_path = os.path.join(in_root, in_cur_relpath)
        out_name = os.path.splitext(in_name)[0]
        out_cur_relpath = os.path.join(out_relpath, out_name.lower())
        slide = tile_slide(pool, in_cur_relpath, in_cur_path, out_name,
                    out_root, out_cur_relpath, stamp)
        if not slide and os.path.splitext(in_cur_path)[1] == '.zip':
            temp_path = mkdtemp(dir=tempdir)
            print 'Extracting %s...' % out_cur_relpath
            zipfile.ZipFile(in_cur_path).extractall(path=temp_path)
            for sub_name in os.listdir(temp_path):
                sub_path = os.path.join(temp_path, sub_name)
                slide = tile_slide(pool, in_cur_relpath, sub_path,
                            out_name, out_root, out_cur_relpath, stamp)
                if slide:
                    break
        if slide:
            slides.append(slide)
    return slides


def tile_tree(in_root, out_root, workers):
    """Generate tiles and metadata for slides in a two-level directory tree."""
    if os.path.exists(os.path.join(out_root, METADATA_NAME)):
        # We want to allow incremental regeneration, but only for recovery
        # from crashes etc.  OpenSlide's rendering of a slide may change
        # over time, so after each OpenSlide release the output tree should
        # be rebuilt from scratch.
        raise ValueError('This is a complete tree; please regenerate from scratch.')
    pool = Pool(workers, generate_pool_init)
    data = {
        'openslide': openslide.__library_version__,
        'openslide_python': openslide.__version__,
        'stamp': sha256('%s %s %s' % (openslide.__library_version__,
                openslide.__version__, STAMP_VERSION)).hexdigest()[:8],
        'groups': [],
    }
    print 'OpenSlide %(openslide)s, OpenSlide Python %(openslide_python)s' % data
    tempdir = mkdtemp(prefix='tiler-', dir='/var/tmp')
    try:
        for in_name in sorted(os.listdir(in_root)):
            if os.path.isdir(os.path.join(in_root, in_name)):
                slides = walk_slides(pool, tempdir, in_root, in_name,
                            out_root, in_name.lower(), data['stamp'])
                if slides:
                    data['groups'].append({
                        'name': GROUP_NAME_MAP.get(in_name, in_name),
                        'slides': slides,
                    })
        with open(os.path.join(out_root, METADATA_NAME), 'w') as fh:
            buf = json.dumps(data, indent=1)
            fh.write('set_slide_info(%s);\n' % buf)
        pool.close()
        pool.join()
    finally:
        shutil.rmtree(tempdir)


def walk_files(root, relpath=''):
    """Return an iterator over files in a directory tree.

    Each iteration yields (directory_relative_path,
    [(file_path, file_relative_path)...])."""

    files = []
    for name in sorted(os.listdir(os.path.join(root, relpath))):
        cur_relpath = os.path.join(relpath, name)
        cur_path = os.path.join(root, cur_relpath)
        if os.path.isdir(cur_path):
            for ent in walk_files(root, cur_relpath):
                yield ent
        else:
            files.append((cur_path, cur_relpath))
    yield (relpath, files)


def upload_pool_init(index):
    global upload_bucket, bucket_index
    conn = boto.connect_s3()
    upload_bucket = conn.get_bucket(S3_BUCKET)
    bucket_index = index


def upload_tile(args):
    path, relpath = args
    if relpath == METADATA_NAME:
        headers = METADATA_HEADERS
    else:
        headers = TILE_HEADERS
    key = boto.s3.key.Key(upload_bucket, relpath)
    with open(path, 'rb') as fh:
        md5_hex, md5_b64 = key.compute_md5(fh)
        if bucket_index.get(relpath, '') != md5_hex:
            key.set_contents_from_file(fh, md5=(md5_hex, md5_b64),
                        policy='public-read', headers=headers)


def sync_tiles(in_root, workers):
    """Synchronize the specified directory tree into S3."""

    if not os.path.exists(os.path.join(in_root, METADATA_NAME)):
        raise ValueError('%s is not a tile directory' % in_root)

    conn = boto.connect_s3()
    bucket = conn.get_bucket(S3_BUCKET)

    print "Storing static files..."
    for relpath, opts in BUCKET_STATIC.iteritems():
        key = boto.s3.key.Key(bucket, relpath)
        key.set_contents_from_string(opts.get('data', ''),
                headers=opts.get('headers', {}), policy='public-read')

    print "Enumerating S3 bucket..."
    index = {}
    for key in bucket.list():
        index[key.name] = key.etag.strip('"')

    print "Pruning S3 bucket..."
    delete = []
    for relpath in sorted(index):
        if (not os.path.exists(os.path.join(in_root, relpath)) and
                relpath not in BUCKET_STATIC):
            delete.append(relpath)
    delete_result = bucket.delete_keys(delete, quiet=True)
    if delete_result.errors:
        raise Exception('Failed to delete %d keys' % len(delete_result.errors))

    pool = Pool(workers, upload_pool_init, [index])
    for parent_relpath, files in walk_files(in_root):
        count = 0
        total = len(files)
        def progress():
            print >> sys.stderr, "Synchronizing %s: %d/%d files\r" % (
                        parent_relpath or 'root', count, total),
        progress()
        for ret in pool.imap_unordered(upload_tile, files, 32):
            count += 1
            if count % 100 == 0:
                progress()
        progress()
        print
    pool.close()
    pool.join()


def sync_info(in_root):
    """Copy info.js from the specified directory tree into S3."""

    conn = boto.connect_s3()
    bucket = conn.get_bucket(S3_BUCKET)
    with open(os.path.join(in_root, METADATA_NAME), 'rb') as fh:
        boto.s3.key.Key(bucket, METADATA_NAME).set_contents_from_file(fh,
                    policy='public-read', headers=METADATA_HEADERS)


if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog [options] {generate|sync|syncinfo} <in_dir>')
    parser.add_option('-j', '--jobs', metavar='COUNT', dest='workers',
                type='int', default=4,
                help='number of worker processes to start [4]')
    parser.add_option('-o', '--output', metavar='DIR', dest='out_root',
                help='output directory')

    (opts, args) = parser.parse_args()
    try:
        command, in_root = args[0:2]
    except ValueError:
        parser.error('Missing argument')

    if command == 'generate':
        if not opts.out_root:
            parser.error('Output directory not specified')
        tile_tree(in_root, opts.out_root, opts.workers)
    elif command == 'sync':
        sync_tiles(in_root, opts.workers)
    elif command == 'syncinfo':
        sync_info(in_root)
    else:
        parser.error('Unknown command')
