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
import shutil
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
        self._path = ''
        self._generators = {}

    def get_dz(self, path, associated=None):
        if path != self._path:
            generator = lambda slide: DeepZoomGenerator(slide, TILE_SIZE,
                        OVERLAP)
            slide = OpenSlide(path)
            self._path = path
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
    try:
        path, associated, level, address, outfile = args
        if not os.path.exists(outfile):
            dz = generator_cache.get_dz(path, associated)
            tile = dz.get_tile(level, address)
            tile.save(outfile, quality=QUALITY)
    except KeyboardInterrupt:
        return KeyboardInterrupt


class DeepZoomImageTiler(object):
    """Handles generation of tiles and metadata for a single image."""

    def __init__(self, pool, path, associated, dz, basename):
        self._pool = pool
        self._path = path
        self._associated = associated
        self._dz = dz
        self._basename = basename

    def run(self):
        count = 0
        total = self._dz.tile_count
        def progress():
            print >> sys.stderr, "Tiling %s: wrote %d/%d tiles\r" % (
                        self._associated or 'slide', count, total),
        progress()
        for ret in self._pool.imap_unordered(process_tile,
                    self._enumerate_tiles(), 32):
            count += 1
            if count % 100 == 0:
                progress()
        progress()
        print
        self._write_dzi()

    def _enumerate_tiles(self):
        for level in xrange(self._dz.level_count):
            tiledir = os.path.join("%s_files" % self._basename, str(level))
            if not os.path.exists(tiledir):
                os.makedirs(tiledir)
            cols, rows = self._dz.level_tiles[level]
            for row in xrange(rows):
                for col in xrange(cols):
                    tilename = os.path.join(tiledir, '%d_%d.%s' % (
                                    col, row, FORMAT))
                    yield (self._path, self._associated, level, (col, row),
                                    tilename)

    def _write_dzi(self):
        with open('%s.dzi' % self._basename, 'w') as fh:
            dzi = self._dz.get_dzi(FORMAT)
            # Hack: add MinTileLevel attribute to Image tag, in violation of
            # the XML schema, to prevent OpenSeadragon from loading the
            # lowest-level tiles
            doc = minidom.parseString(dzi)
            doc.documentElement.setAttribute('MinTileLevel', '8')
            fh.write(doc.toxml('UTF-8'))


class DeepZoomSlideTiler(object):
    """Handles generation of tiles and metadata for all images in a slide."""

    def __init__(self, pool, slidepath, basename):
        self._pool = pool
        self._path = slidepath
        self._slide = OpenSlide(slidepath)
        self._basename = basename

    def run(self):
        self._run_image()
        for name in self._slide.associated_images:
            self._run_image(name)
        self._write_html()
        self._write_static()

    def _run_image(self, associated=None):
        """Run a single image from self._slide."""
        if associated is None:
            image = self._slide
            basename = os.path.join(self._basename, VIEWER_SLIDE_NAME)
        else:
            image = ImageSlide(self._slide.associated_images[associated])
            basename = os.path.join(self._basename, self._slugify(associated))
        dz = DeepZoomGenerator(image, TILE_SIZE, OVERLAP)
        DeepZoomImageTiler(self._pool, self._path, associated, dz,
                    basename).run()

    def _url_for(self, associated):
        if associated is None:
            base = VIEWER_SLIDE_NAME
        else:
            base = self._slugify(associated)
        return '%s.dzi' % base

    def _write_html(self):
        env = jinja2.Environment(loader=jinja2.PackageLoader(__name__),
                    autoescape=True)
        template = env.get_template('index.html')
        associated_urls = dict((n, self._url_for(n))
                    for n in self._slide.associated_images)
        data = template.render(slide_url=self._url_for(None),
                    associated=associated_urls,
                    properties=self._slide.properties)
        with open(os.path.join(self._basename, 'index.html'), 'w') as fh:
            fh.write(data)

    def _write_static(self):
        basesrc = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    'static')
        basedst = os.path.join(self._basename, 'static')
        self._copydir(basesrc, basedst)
        self._copydir(os.path.join(basesrc, 'images'),
                    os.path.join(basedst, 'images'))

    def _copydir(self, src, dest):
        if not os.path.exists(dest):
            os.makedirs(dest)
        for name in os.listdir(src):
            srcpath = os.path.join(src, name)
            if os.path.isfile(srcpath):
                shutil.copy(srcpath, os.path.join(dest, name))

    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    @classmethod
    def _slugify(cls, text):
        """Generates an ASCII-only slug."""
        # Based on Flask snippet 5
        result = []
        for word in cls._punct_re.split(unicode(text, 'UTF-8').lower()):
            word = normalize('NFKD', word).encode('ascii', 'ignore')
            if word:
                result.append(word)
        return unicode(u'_'.join(result))


class DeepZoomStaticTiler(object):
    """Generates tiles and metadata for all slides in a directory tree."""

    def __init__(self, path, basename, workers):
        self._path = slidepath
        self._basename = basename
        self._pool = Pool(workers, pool_init)

    def run(self):
        self._walk_dir(self._path, self._basename)
        self._pool.close()
        self._pool.join()

    def _walk_dir(self, in_base, out_base):
        for in_name in os.listdir(in_base):
            in_path = os.path.join(in_base, in_name)
            out_path = os.path.join(out_base, in_name.lower())
            if os.path.isdir(in_path):
                self._walk_dir(in_path, out_path)
            elif OpenSlide.can_open(in_path):
                DeepZoomSlideTiler(self._pool, in_path, out_path).run()


if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog [options] <slide>')
    parser.add_option('-j', '--jobs', metavar='COUNT', dest='workers',
                type='int', default=4,
                help='number of worker processes to start [4]')
    parser.add_option('-o', '--output', metavar='NAME', dest='basename',
                help='base name of output file')

    (opts, args) = parser.parse_args()
    try:
        slidepath = args[0]
    except IndexError:
        parser.error('Missing slide argument')
    if opts.basename is None:
        opts.basename = os.path.splitext(os.path.basename(slidepath))[0]

    DeepZoomStaticTiler(slidepath, opts.basename, opts.workers).run()
