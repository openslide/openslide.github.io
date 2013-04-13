#!/usr/bin/env python
#
# _upload - Upload a new file to download.openslide.org
#
# Copyright (c) 2010-2013 Carnegie Mellon University
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
import mimetypes
from optparse import OptionParser
import os
import posixpath
import re

S3_BUCKET = 'download.openslide.org'

# Avoid calling .tar.gz "application/x-tar"
mimetypes.encodings_map = {}
mimetypes.init()


def local_to_remote_path(path):
    filename = os.path.basename(path)
    patterns = (
        ('openslide-[0-9.]+\.tar\.(gz|xz)$',
                '/releases/openslide'),
        ('openslide-java-[0-9.]+\.tar\.(gz|xz)$',
                '/releases/openslide-java'),
        ('openslide-python-[0-9.]+\.tar\.(gz|xz)$',
                '/releases/openslide-python'),
        ('openslide-win(build|32|64)-[0-9]{8}\.zip$',
                '/releases/openslide-winbuild'),
    )
    for pattern, directory in patterns:
        if re.match(pattern, filename):
            return posixpath.join(directory, filename)
    return None


def upload(paths):
    conn = boto.connect_s3()
    bucket = conn.get_bucket(S3_BUCKET)
    to_upload = []

    for path in paths:
        remote_path = local_to_remote_path(path)
        if not remote_path:
            result = '[unknown; skipped]'
        else:
            key = bucket.new_key(remote_path)
            if key.exists():
                result = '[duplicate; skipped]'
            else:
                result = posixpath.dirname(remote_path)
                to_upload.append((path, key))
        print '%-35s -> %s' % (os.path.basename(path), result)

    if raw_input('\nOK (y/n)? ') != 'y':
        return

    for path, key in to_upload:
        content_type = (mimetypes.guess_type(path)[0] or
                'application/octet-stream')
        print '%-35s %s' % (os.path.basename(path), content_type)
        key.set_contents_from_filename(path, policy='public-read',
                headers={'Content-Type': content_type})


if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog <files>')
    (opts, args) = parser.parse_args()
    upload(args)
