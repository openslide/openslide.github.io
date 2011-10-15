#!/usr/bin/env python
#
# deepzoom-tile - Convert whole-slide images to Deep Zoom format
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

"""An example program to generate a Deep Zoom directory tree from a slide."""

import jinja2
from multiprocessing import Pool
from openslide import OpenSlide, ImageSlide
from openslide.deepzoom import DeepZoomGenerator
from optparse import OptionParser
import os
import re
import sys
from unicodedata import normalize
import xml.dom.minidom as minidom

VIEWER_SLIDE_NAME = 'slide'
FORMAT = 'jpeg'
QUALITY = 75
TILE_SIZE = 512
OVERLAP = 1

class GeneratorCache(object):
    def __init__(self):
        self._slidepath = ''
        self._generators = {}

    def get_dz(self, slidepath, associated=None):
        if slidepath != self._slidepath:
            generator = lambda slide: DeepZoomGenerator(slide, TILE_SIZE,
                        OVERLAP)
            slide = OpenSlide(slidepath)
            self._slidepath = slidepath
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
        slidepath, associated, level, address, outfile = args
        if not os.path.exists(outfile):
            dz = generator_cache.get_dz(slidepath, associated)
            tile = dz.get_tile(level, address)
            tile.save(outfile, quality=QUALITY)
    except KeyboardInterrupt:
        return KeyboardInterrupt


def enumerate_tiles(slidepath, associated, dz, out_base):
    """Enumerate tiles in a single image."""
    for level in xrange(dz.level_count):
        tiledir = os.path.join("%s_files" % out_base, str(level))
        if not os.path.exists(tiledir):
            os.makedirs(tiledir)
        cols, rows = dz.level_tiles[level]
        for row in xrange(rows):
            for col in xrange(cols):
                tilename = os.path.join(tiledir, '%d_%d.%s' % (
                                col, row, FORMAT))
                yield (slidepath, associated, level, (col, row), tilename)


def tile_image(pool, slidepath, associated, dz, out_base):
    """Generate tiles and metadata for a single image."""

    count = 0
    total = dz.tile_count
    iterator = enumerate_tiles(slidepath, associated, dz, out_base)

    def progress():
        print >> sys.stderr, "Tiling %s %s: wrote %d/%d tiles\r" % (
                    os.path.basename(slidepath), associated or 'slide',
                    count, total),

    # Write tiles
    progress()
    for ret in pool.imap_unordered(process_tile, iterator, 32):
        count += 1
        if count % 100 == 0:
            progress()
    progress()
    print

    # Write DZI
    with open('%s.dzi' % out_base, 'w') as fh:
        dzi = dz.get_dzi(FORMAT)
        # Hack: add MinTileLevel attribute to Image tag, in violation of
        # the XML schema, to prevent OpenSeadragon from loading the
        # lowest-level tiles
        doc = minidom.parseString(dzi)
        doc.documentElement.setAttribute('MinTileLevel', '8')
        fh.write(doc.toxml('UTF-8'))


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


def dzi_for(associated=None):
    """Return the name of the DZI file for an image."""
    if associated is None:
        base = VIEWER_SLIDE_NAME
    else:
        base = slugify(associated)
    return '%s.dzi' % base


def tile_slide(pool, slidepath, out_base):
    """Generate tiles and metadata for all images in a slide."""

    slide = OpenSlide(slidepath)

    # Process images
    def do_tile(associated, image, out_base):
        dz = DeepZoomGenerator(image, TILE_SIZE, OVERLAP)
        tile_image(pool, slidepath, associated, dz, out_base)
    do_tile(None, slide, os.path.join(out_base, VIEWER_SLIDE_NAME))
    for associated, image in slide.associated_images.iteritems():
        do_tile(associated, ImageSlide(image), os.path.join(out_base,
                    slugify(associated)))

    # Write HTML
    env = jinja2.Environment(loader=jinja2.PackageLoader(__name__),
                autoescape=True)
    template = env.get_template('index.html')
    associated_urls = dict((n, dzi_for(n)) for n in slide.associated_images)
    data = template.render(slide_url=dzi_for(None),
                associated=associated_urls,
                properties=slide.properties)
    with open(os.path.join(out_base, 'index.html'), 'w') as fh:
        fh.write(data)


def walk_dir(pool, in_base, out_base):
    """Build a directory tree of tiled images from a tree of slides."""
    for in_name in os.listdir(in_base):
        in_path = os.path.join(in_base, in_name)
        out_path = os.path.join(out_base, in_name.lower())
        if os.path.isdir(in_path):
            walk_dir(pool, in_path, out_path)
        elif OpenSlide.can_open(in_path):
            tile_slide(pool, in_path, out_path)


def tile_tree(in_base, out_base, workers):
    """Generate tiles and metadata for all slides in a directory tree."""
    pool = Pool(workers, pool_init)
    walk_dir(pool, in_base, out_base)
    pool.close()
    pool.join()


if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog [options] <in_dir> <out_dir>')
    parser.add_option('-j', '--jobs', metavar='COUNT', dest='workers',
                type='int', default=4,
                help='number of worker processes to start [4]')

    (opts, args) = parser.parse_args()
    try:
        in_base, out_base = args[0:2]
    except IndexError:
        parser.error('Missing argument')

    tile_tree(in_base, out_base, opts.workers)
