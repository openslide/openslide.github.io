#!/usr/bin/env python
#
# _synctiles - Generate and upload Deep Zoom tiles for test slides
#
# Copyright (c) 2010-2011 Carnegie Mellon University
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
import json
from multiprocessing import Pool
import openslide
from openslide import OpenSlide, ImageSlide
from openslide.deepzoom import DeepZoomGenerator
from optparse import OptionParser
import os
import re
import shutil
import sys
from tempfile import mkdtemp
from unicodedata import normalize
import xml.dom.minidom as minidom
import zipfile

S3_BUCKET = 'openslide-demo'
BASE_URL = 'http://%s.s3.amazonaws.com/' % S3_BUCKET
DOWNLOAD_BASE_URL = 'http://openslide.cs.cmu.edu/download/openslide-testdata/'
VIEWER_SLIDE_NAME = 'slide'
METADATA_NAME = 'info.js'
SLIDE_METADATA_NAME = 'properties.js'
FORMAT = 'jpeg'
QUALITY = 75
TILE_SIZE = 512
OVERLAP = 1
GROUP_NAME_MAP = {
    'Generic-TIFF': 'Generic TIFF',
    'Hamamatsu': 'Hamamatsu NDPI',
    'Hamamatsu-vms': 'Hamamatsu VMS',
    'Mirax': 'MIRAX',
}


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text):
    """Generate an ASCII-only slug."""
    # Based on Flask snippet 5
    result = []
    for word in _punct_re.split(unicode(text, 'UTF-8').lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(u'_'.join(result))


class GeneratorCache(object):
    def __init__(self):
        self._in_path = ''
        self._generators = {}

    def get_dz(self, in_path, associated=None):
        if in_path != self._in_path:
            generator = lambda slide: DeepZoomGenerator(slide, TILE_SIZE,
                        OVERLAP)
            slide = OpenSlide(in_path)
            self._in_path = in_path
            self._generators = {
                None: generator(slide)
            }
            for name, image in slide.associated_images.iteritems():
                self._generators[name] = generator(ImageSlide(image))
        return self._generators[associated]


def pool_init():
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

    # Format DZI
    dzi = dz.get_dzi(FORMAT)
    # Hack: add MinTileLevel attribute to Image tag, in violation of
    # the XML schema, to prevent OpenSeadragon from loading the
    # lowest-level tiles
    doc = minidom.parseString(dzi)
    doc.documentElement.setAttribute('MinTileLevel', '8')
    dzi = doc.toxml('UTF-8')

    # Return properties
    return {
        'name': associated,
        'dzi': dzi,
        'url': os.path.join(BASE_URL, out_relpath + '.dzi'),
    }


def tile_slide(pool, in_relpath, in_phys_path, out_name, out_root,
            out_relpath):
    """Generate tiles and metadata for all images in a slide."""
    slide = OpenSlide(in_phys_path)
    def do_tile(associated, image, out_relpath):
        dz = DeepZoomGenerator(image, TILE_SIZE, OVERLAP)
        return tile_image(pool, in_phys_path, associated, dz, out_root,
                    out_relpath)
    properties = {
        'name': out_name,
        'slide': do_tile(None, slide,
                    os.path.join(out_relpath, VIEWER_SLIDE_NAME)),
        'associated': [],
        'properties_url': os.path.join(BASE_URL, out_relpath,
                    SLIDE_METADATA_NAME),
        'download_url': os.path.join(DOWNLOAD_BASE_URL, in_relpath),
    }
    for associated, image in sorted(slide.associated_images.items()):
        cur_props = do_tile(associated, ImageSlide(image),
                    os.path.join(out_relpath, slugify(associated)))
        properties['associated'].append(cur_props)
    with open(os.path.join(out_root, out_relpath, SLIDE_METADATA_NAME),
                'w') as fh:
        buf = json.dumps(dict(slide.properties), indent=1)
        fh.write('set_slide_properties(%s);\n' % buf)
    return properties


def walk_slides(pool, tempdir, in_root, in_relpath, out_root, out_relpath):
    """Build a directory of tiled images from a directory of slides."""
    slides = []
    for in_name in sorted(os.listdir(os.path.join(in_root, in_relpath))):
        in_cur_relpath = os.path.join(in_relpath, in_name)
        in_cur_path = os.path.join(in_root, in_cur_relpath)
        out_name = os.path.splitext(in_name)[0]
        out_cur_relpath = os.path.join(out_relpath, out_name.lower())
        if OpenSlide.can_open(in_cur_path):
            slides.append(tile_slide(pool, in_cur_relpath, in_cur_path,
                        out_name, out_root, out_cur_relpath))
        elif os.path.splitext(in_cur_path)[1] == '.zip':
            temp_path = mkdtemp(dir=tempdir)
            print 'Extracting %s...' % out_cur_relpath
            zipfile.ZipFile(in_cur_path).extractall(path=temp_path)
            for sub_name in os.listdir(temp_path):
                sub_path = os.path.join(temp_path, sub_name)
                if OpenSlide.can_open(sub_path):
                    slides.append(tile_slide(pool, in_cur_relpath, sub_path,
                                out_name, out_root, out_cur_relpath))
                    break
    return slides


def tile_tree(in_root, out_root, workers):
    """Generate tiles and metadata for slides in a two-level directory tree."""
    if os.path.exists(os.path.join(out_root, METADATA_NAME)):
        # We want to allow incremental regeneration, but only for recovery
        # from crashes etc.  OpenSlide's rendering of a slide may change
        # over time, so after each OpenSlide release the output tree should
        # be rebuilt from scratch.
        raise ValueError('This is a complete tree; please regenerate from scratch.')
    pool = Pool(workers, pool_init)
    data = {
        'openslide': openslide.__library_version__,
        'openslide_python': openslide.__version__,
        'groups': [],
    }
    print 'OpenSlide %(openslide)s, OpenSlide Python %(openslide_python)s' % data
    tempdir = mkdtemp(prefix='tiler-')
    try:
        for in_name in sorted(os.listdir(in_root)):
            if os.path.isdir(os.path.join(in_root, in_name)):
                slides = walk_slides(pool, tempdir, in_root, in_name,
                            out_root, in_name.lower())
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


def sync_tiles(in_root):
    """Synchronize the specified directory tree into S3."""

    if not os.path.exists(os.path.join(in_root, METADATA_NAME)):
        raise ValueError('%s is not a tile directory' % in_root)

    conn = boto.connect_s3()
    bucket = conn.get_bucket(S3_BUCKET)

    print "Enumerating S3 bucket..."
    index = {}
    for key in bucket.list():
        index[key.name] = key.etag.strip('"')

    print "Pruning S3 bucket..."
    for relpath in sorted(index):
        if not os.path.exists(os.path.join(in_root, relpath)):
            boto.s3.key.Key(bucket, relpath).delete()

    for parent_relpath, files in walk_files(in_root):
        count = 0
        total = len(files)
        for cur_path, cur_relpath in files:
            key = boto.s3.key.Key(bucket, cur_relpath)
            with open(cur_path, 'rb') as fh:
                md5_hex, md5_b64 = key.compute_md5(fh)
                if index.get(cur_relpath, '') != md5_hex:
                    key.set_contents_from_file(fh, md5=(md5_hex, md5_b64),
                                policy='public-read')
            count += 1
            print >> sys.stderr, "Synchronizing %s: %d/%d files\r" % (
                        parent_relpath or 'root', count, total),
        if total:
            print


def sync_info(in_root):
    """Copy info.js from the specified directory tree into S3."""

    conn = boto.connect_s3()
    bucket = conn.get_bucket(S3_BUCKET)
    with open(os.path.join(in_root, METADATA_NAME), 'rb') as fh:
        boto.s3.key.Key(bucket, METADATA_NAME).set_contents_from_file(fh,
                    policy='public-read')


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
        sync_tiles(in_root)
    elif command == 'syncinfo':
        sync_info(in_root)
    else:
        parser.error('Unknown command')
