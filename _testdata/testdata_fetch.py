#!/usr/bin/env python3
#
# testdata_fetch - Fetch openslide-testdata to local directory
#
# Copyright (c) 2010-2015,2022 Carnegie Mellon University
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

from __future__ import annotations

import argparse
import calendar
from hashlib import sha256
import json
import os
from pathlib import Path, PurePath
from typing import cast
from urllib.parse import urljoin

import dateutil.parser
import requests

TESTDATA_BASEURL = 'https://openslide.cs.cmu.edu/download/openslide-testdata/'
BUFSIZE = 10 << 20
IGNORE_FILENAMES = frozenset(
    (
        'index.html',
        'index.json',
        'index.yaml',
    )
)


def fetch_file(
    baseurl: str,
    basepath: Path,
    relpath: PurePath,
    expected_sha256: str | None = None,
) -> Path:
    path = basepath / relpath
    count = 0
    sha = sha256()

    r = requests.get(urljoin(baseurl, relpath.as_posix()), stream=True)
    r.raise_for_status()

    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open('wb') as fh:
            for buf in r.iter_content(BUFSIZE):
                fh.write(buf)
                if expected_sha256 is not None:
                    sha.update(buf)
                count += len(buf)
        if count != int(r.headers['Content-Length']):
            raise OSError(f"Short read fetching {relpath}")
        if expected_sha256 is not None and expected_sha256 != sha.hexdigest():
            raise OSError(f'Hash mismatch fetching {relpath}')
    except Exception:
        path.unlink()
        raise

    try:
        dt = dateutil.parser.parse(r.headers['Last-Modified'])
        stamp = calendar.timegm(dt.utctimetuple())
        os.utime(path, (stamp, stamp))
    except KeyError:
        pass

    return path


def fetch_slide(
    baseurl: str,
    basepath: Path,
    relpath: PurePath,
    info: dict[str, str | int],
    check_hashes: bool = False,
) -> Path:
    path = basepath / relpath
    try:
        if path.stat().st_size == info['size']:
            # File already exists and is the right size
            if not check_hashes:
                # Assume identical to remote
                return path
            with path.open('rb') as fh:
                sha = sha256()
                while True:
                    buf = fh.read(BUFSIZE)
                    if not buf:
                        break
                    sha.update(buf)
            if sha.hexdigest() == info['sha256']:
                # Identical to remote
                return path
    except OSError:
        # No local copy
        pass

    print(f'Fetching {relpath}...')
    return fetch_file(baseurl, basepath, relpath, cast(str, info['sha256']))


def fetch_repo(
    basepath: Path, baseurl: str = TESTDATA_BASEURL, check_hashes: bool = False
) -> None:
    # Fetch JSON index
    jsonpath = fetch_file(baseurl, basepath, PurePath('index.json'))
    with jsonpath.open() as fh:
        slides = json.load(fh)

    # Fetch slides
    dirpaths = set()
    for rp, info in sorted(slides.items()):
        relpath = PurePath(rp)
        fetch_slide(
            baseurl, basepath, relpath, info, check_hashes=check_hashes
        )
        dirpaths.add(relpath.parent)

    # Fetch YAML metadata
    for dirpath in sorted(dirpaths):
        fetch_file(baseurl, basepath, dirpath / 'index.yaml')

    # Check for extra files in local repo
    for filepath in basepath.rglob('*'):
        if (
            filepath.is_file()
            and filepath.relative_to(basepath).as_posix() not in slides
            and filepath.name not in IGNORE_FILENAMES
        ):
            print(f'Unexpected file: {filepath}')


def _main() -> None:
    parser = argparse.ArgumentParser(
        description='Fetch openslide-testdata to local directory.'
    )
    parser.add_argument(
        'path', type=Path, help='path to destination directory'
    )
    parser.add_argument(
        '-c',
        '--check-hashes',
        action='store_true',
        help='check SHA-256 digests of existing files',
    )
    args = parser.parse_args()
    fetch_repo(args.path, check_hashes=args.check_hashes)


if __name__ == '__main__':
    _main()
