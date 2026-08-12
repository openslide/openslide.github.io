#!/usr/bin/env python3
#
# testdata_zip - Create ZIP archive for multi-file testdata slide
#
# Copyright (c) 2026 Benjamin Gilbert
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of version 2.1 of the GNU Lesser General Public License
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path
from shutil import copyfileobj
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile, ZipInfo


def add_member(zf: ZipFile, root: Path, path: Path) -> None:
    info = ZipInfo.from_file(path, path.relative_to(root))
    if info.is_dir():
        info.compress_type = ZIP_STORED
        info.external_attr = (0o40755 << 16) | 0x10
        zf.writestr(info, b'')
    else:
        info.compress_type = ZIP_DEFLATED
        info.compress_level = 9
        info.external_attr = 0o100644 << 16
        with path.open('rb') as rh, zf.open(info, 'w') as wh:
            copyfileobj(rh, wh)


def create_zip(path: Path) -> None:
    def on_error(err: OSError) -> None:
        raise err

    zip_path = path.with_suffix('.zip')
    with ZipFile(zip_path, 'w') as zf:
        for dirpath, dirnames, filenames in path.walk(on_error=on_error):
            dirnames.sort()
            if dirpath != path:
                add_member(zf, path, dirpath)
            for filename in sorted(filenames):
                add_member(zf, path, dirpath / filename)

    with zip_path.open('rb') as fh:
        hash = sha256()
        while True:
            buf = fh.read(1 << 20)
            if not buf:
                break
            hash.update(buf)
        print(hash.hexdigest())


def _main() -> None:
    parser = argparse.ArgumentParser(
        description='Create openslide-testdata ZIP from specified directory.'
    )
    parser.add_argument('path', type=Path, help='path to source directory')
    args = parser.parse_args()
    create_zip(args.path)


if __name__ == '__main__':
    _main()
