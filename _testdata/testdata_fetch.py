#!/usr/bin/python
#
# testdata_fetch - Fetch openslide-testdata to local directory
#
# Copyright (c) 2010-2015 Carnegie Mellon University
#
# This program is free software; you can redistribute it and/or modify it
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

import argparse
import calendar
import dateutil.parser
from hashlib import sha256
import json
import os
import requests
from urlparse import urljoin

TESTDATA_BASEURL = 'https://openslide.cs.cmu.edu/download/openslide-testdata/'
BUFSIZE = 10 << 20
IGNORE_FILENAMES = frozenset((
    'index.html',
    'index.json',
    'index.yaml',
))

def fetch_file(baseurl, basepath, relpath, expected_sha256=None):
    path = os.path.join(basepath, relpath)
    dirpath = os.path.dirname(path)
    count = 0
    sha = sha256()

    r = requests.get(urljoin(baseurl, relpath), stream=True)
    r.raise_for_status()
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    try:
        with open(path, 'wb') as fh:
            for buf in r.iter_content(BUFSIZE):
                fh.write(buf)
                if expected_sha256 is not None:
                    sha.update(buf)
                count += len(buf)
        if count != int(r.headers['Content-Length']):
            raise IOError("Short read fetching %s" % relpath)
        if expected_sha256 is not None and expected_sha256 != sha.hexdigest():
            raise IOError('Hash mismatch fetching %s' % relpath)
    except Exception:
        os.unlink(path)
        raise

    try:
        dt = dateutil.parser.parse(r.headers['Last-Modified'])
        stamp = calendar.timegm(dt.utctimetuple())
        os.utime(path, (stamp, stamp))
    except KeyError:
        pass

    return path


def fetch_slide(baseurl, basepath, relpath, info, check_hashes=False):
    path = os.path.join(basepath, relpath)
    try:
        if os.stat(path).st_size == info['size']:
            # File already exists and is the right size
            if not check_hashes:
                # Assume identical to remote
                return
            with open(path, 'rb') as fh:
                sha = sha256()
                while True:
                    buf = fh.read(BUFSIZE)
                    if not buf:
                        break
                    sha.update(buf)
            if sha.hexdigest() == info['sha256']:
                # Identical to remote
                return
    except OSError:
        # No local copy
        pass

    print 'Fetching %s...' % relpath
    fetch_file(baseurl, basepath, relpath, info['sha256'])


def fetch_repo(basepath, baseurl=TESTDATA_BASEURL, check_hashes=False):
    # Fetch JSON index
    jsonpath = fetch_file(baseurl, basepath, 'index.json')
    with open(jsonpath) as fh:
        slides = json.load(fh)

    # Fetch slides
    dirpaths = set()
    for relpath, info in sorted(slides.items()):
        fetch_slide(baseurl, basepath, relpath, info,
                check_hashes=check_hashes)
        dirpaths.add('/'.join(relpath.split('/')[:-1]))

    # Fetch YAML metadata
    for dirpath in sorted(dirpaths):
        fetch_file(baseurl, basepath, dirpath + '/index.yaml')

    # Check for extra files in local repo
    for dirpath, dirnames, filenames in os.walk(basepath):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if (filepath[len(basepath):].lstrip('/') not in slides
                    and filename not in IGNORE_FILENAMES):
                print 'Unexpected file: %s' % filepath


def _main():
    parser = argparse.ArgumentParser(description='Fetch openslide-testdata ' +
            'to local directory.')
    parser.add_argument('path',
            help='path to destination directory')
    parser.add_argument('-c', '--check-hashes', action='store_true',
            help='check SHA-256 digests of existing files')
    args = parser.parse_args()
    fetch_repo(args.path, check_hashes=args.check_hashes)


if __name__ == '__main__':
    _main()
