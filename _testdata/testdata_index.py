#!/usr/bin/python
#
# testdata_index - Check metadata and build indexes for openslide-testdata
#
# Copyright (c) 2013-2015 Carnegie Mellon University
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

from __future__ import division
import argparse
from hashlib import sha256
from jinja2 import Environment, Template
import json
import os
import yaml

IGNORE_FILENAMES = frozenset((
    'index.html',
    'index.yaml',
))
MANDATORY_FIELDS = frozenset((
    'description',
    'sha256',
))
OPTIONAL_FIELDS = frozenset((
    'credit',
))

INDEX_TEMPLATE = '''<!doctype html>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
<style type="text/css">
table {
  margin-left: 20px;
  border-collapse: collapse;
}
tr:nth-child(2n + 3) {
  background: #f4f4f4;
}
td {
  padding-top: 0.5em;
  padding-bottom: 0.5em;
  padding-right: 20px;
}
td.filename {
  white-space: nowrap;
}
td.size {
  white-space: nowrap;
  text-align: right;
}
.filetype {
  text-align: center;
  width: 1em;
  margin-right: 5px;
}
</style>
<title>{{ title }}</title>
<h1>{{ title }}</h1>
<table>
  <tr>
    <th>Name</th>
    <th>Size</th>
    <th>Description</th>
    <th>Credit</th>
  </tr>
  {% macro row(icon, href, name, size='', description='', credit='') %}
    <tr>
      <td class="filename">
        <i class="filetype fa {{ icon }}"></i>
        <a href="{{ href }}">{{ name }}</a>
      </td>
      <td class="size">{{ size }}</td>
      <td class="description">{{ description }}</td>
      <td class="credit">{{ credit }}</td>
    </tr>
  {% endmacro %}
  {% if has_parent %}
    {{ row('fa-level-up', '..', '[Parent Directory]') }}
  {% endif %}
  {% for name, description in (dirs or {}).items()|sort %}
    {{ row('fa-folder', name + '/', name, description=description) }}
  {% endfor %}
  {% for name, info in (files or {}).items()|sort %}
    {{ row('fa-file-archive-o' if name.endswith('.zip') else 'fa-file-image-o',
        name, name, info.size|file_size_units, info.description,
        info.credit) }}
  {% endfor %}
  {% for extra in extras %}
    {{ row('fa-file-code-o', extra.name, extra.name,
        extra.size|file_size_units, extra.description) }}
  {% endfor %}
</table>
'''


class ValidationError(Exception):
    pass


def file_size_units(value):
    for shift, unit in (40, 'TB'), (30, 'GB'), (20, 'MB'), (10, 'KB'):
        if value >= (1 << shift):
            in_units = value / (1 << shift)
            return ('%.2f' % in_units).rstrip('0').rstrip('.') + ' ' + unit
    return '%d bytes' % value


environment = Environment(autoescape=True)
environment.filters['file_size_units'] = file_size_units
index_template = environment.from_string(INDEX_TEMPLATE)


def ensure_empty(items, msg_prefix):
    if items:
        raise ValidationError('%s: %s' % (msg_prefix,
                ', '.join(sorted(items))))


def process_dir(dirpath, check_hashes=False):
    # List files in directory
    filenames = set(os.listdir(dirpath)) - IGNORE_FILENAMES

    # Load metadata
    yamlpath = os.path.join(dirpath, 'index.yaml')
    with open(yamlpath, 'rb') as fh:
        info = yaml.safe_load(fh)
        description = info['description']
        slides = info['slides']

    # Check slides against directory
    slide_names = set(slides.keys())
    ensure_empty(filenames - slide_names,
            'Missing files in index for %s' % dirpath)
    ensure_empty(slide_names - filenames,
            'Missing files in directory %s' % dirpath)

    # Check metadata fields and populate sizes
    for filename, info in sorted(slides.items()):
        filepath = os.path.join(dirpath, filename)
        info_fields = set(info.keys())
        ensure_empty(info_fields - MANDATORY_FIELDS - OPTIONAL_FIELDS,
                '%s: Unknown fields' % filepath)
        ensure_empty(MANDATORY_FIELDS - info_fields,
                '%s: Missing mandatory fields' % filepath)
        if check_hashes:
            sha = sha256()
            with open(filepath, 'rb') as fh:
                while True:
                    buf = fh.read(10 << 20)
                    if not buf:
                        break
                    sha.update(buf)
                if sha.hexdigest() != info['sha256']:
                    raise ValidationError('%s: Hash mismatch' % filepath)
        info['size'] = os.stat(filepath).st_size

    # Write index.html
    with open(os.path.join(dirpath, 'index.html'), 'w') as fh:
        index_template.stream(
            has_parent=True,
            title=description,
            files=slides,
            extras=[
                {
                    'name': 'index.yaml',
                    'description': 'Slide metadata',
                    'size': os.stat(yamlpath).st_size,
                },
            ],
        ).dump(fh)

    return description, slides


def process_repo(basepath, check_hashes=False):
    # Enumerate directory names
    dirnames = [name for name in sorted(os.listdir(basepath))
            if os.path.isdir(os.path.join(basepath, name))]

    # Descend into directories
    dir_descs = {}
    slides = {}
    for dirname in dirnames:
        dirpath = os.path.join(basepath, dirname)
        dir_desc, dir_slides = process_dir(dirpath, check_hashes=check_hashes)
        dir_descs[dirname] = dir_desc
        for filename, info in dir_slides.items():
            slides['%s/%s' % (dirname, filename)] = info

    # Write index.json
    jsonpath = os.path.join(basepath, 'index.json')
    with open(jsonpath, 'w') as fh:
        json.dump(slides, fh, indent=2, sort_keys=True)

    # Write index.html
    with open(os.path.join(basepath, 'index.html'), 'w') as fh:
        index_template.stream(
            title='openslide-testdata',
            dirs=dir_descs,
            extras=[
                {
                    'name': 'index.json',
                    'description': 'Consolidated metadata for all slides',
                    'size': os.stat(jsonpath).st_size,
                },
            ],
        ).dump(fh)


def _main():
    parser = argparse.ArgumentParser(description='Process metadata and ' +
            'build indexes for openslide-testdata.')
    parser.add_argument('path',
            help='path to local copy of openslide-testdata')
    parser.add_argument('-c', '--check-hashes', action='store_true',
            help='check SHA-256 digests')
    args = parser.parse_args()
    process_repo(args.path, check_hashes=args.check_hashes)


if __name__ == '__main__':
    _main()
