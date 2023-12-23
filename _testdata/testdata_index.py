#!/usr/bin/env python3
#
# testdata_index - Check metadata and build indexes for openslide-testdata
#
# Copyright (c) 2013-2015,2022 Carnegie Mellon University
# Copyright (c) 2016 Benjamin Gilbert
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
from hashlib import sha256
import json
import os
from pathlib import Path

from jinja2 import Environment, Template
import yaml

IGNORE_FILENAMES = frozenset(
    (
        'index.html',
        'index.yaml',
    )
)
MANDATORY_FIELDS = frozenset(
    (
        'description',
        'license',
        'sha256',
    )
)
OPTIONAL_FIELDS = frozenset(('credit',))

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
th {
  padding-left: 10px;
  padding-right: 10px;
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
    <th>License</th>
    <th>Credit</th>
  </tr>
  {% macro row(icon, href, name, size='', description='', license='',
      credit='') %}
    <tr>
      <td class="filename">
        <i class="filetype fa {{ icon }}"></i>
        <a href="{{ href }}">{{ name }}</a>
      </td>
      <td class="size">{{ size }}</td>
      <td class="description">{{ description }}</td>
      <td class="license">
        {% if license == 'distributable' %}
          Free to use and distribute, with or without modification
        {% elif license == 'CC0-1.0' %}
          <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a>
        {% elif license == 'CC0-1.0-with-OpenSeadragon' %}
          <a href="https://openseadragon.github.io/license/">3-clause BSD</a>
          for bundled OpenSeadragon,
          <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a>
          otherwise
        {% elif license != '' %}
          Unknown
        {% endif %}
      </td>
      <td class="credit">{{ credit }}</td>
    </tr>
  {% endmacro %}
  {% if has_parent %}
    {{ row('fa-level-up', '..', '[Parent Directory]') }}
  {% endif %}
  {% for name, format in (dirs or {}).items()|sort %}
    {{ row('fa-folder', name + '/', name, description=format) }}
  {% endfor %}
  {% for name, info in (files or {}).items()|sort %}
    {{ row('fa-file-archive-o' if name.endswith('.zip') else 'fa-file-image-o',
        name, name, info.size|file_size_units, info.description,
        info.license, info.credit) }}
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
    for shift, unit in (40, ' TB'), (30, ' GB'), (20, ' MB'), (10, ' KB'):
        if value >= (1 << shift):
            in_units = value / (1 << shift)
            return f'{in_units:.2f}'.rstrip('0').rstrip('.') + unit
    return f'{value} bytes'


environment = Environment(autoescape=True)
environment.filters['file_size_units'] = file_size_units
index_template = environment.from_string(INDEX_TEMPLATE)


def ensure_empty(items, msg_prefix):
    if items:
        raise ValidationError(
            '{}: {}'.format(msg_prefix, ', '.join(sorted(items)))
        )


def process_dir(dirpath, check_hashes=False):
    # List files in directory
    filenames = set(path.name for path in dirpath.iterdir()) - IGNORE_FILENAMES

    # Load metadata
    yamlpath = dirpath / 'index.yaml'
    with open(yamlpath, 'rb') as fh:
        info = yaml.safe_load(fh)
        format_ = info['format']
        slides = info['slides']

    # Check slides against directory
    slide_names = set(slides.keys())
    ensure_empty(
        filenames - slide_names, f'Missing files in index for {dirpath}'
    )
    ensure_empty(
        slide_names - filenames, f'Missing files in directory {dirpath}'
    )

    # Check metadata fields and populate sizes
    for filename, info in sorted(slides.items()):
        filepath = dirpath / filename
        info_fields = set(info.keys())
        ensure_empty(
            info_fields - MANDATORY_FIELDS - OPTIONAL_FIELDS,
            f'{filepath}: Unknown fields',
        )
        ensure_empty(
            MANDATORY_FIELDS - info_fields,
            f'{filepath}: Missing mandatory fields',
        )
        if check_hashes:
            sha = sha256()
            with open(filepath, 'rb') as fh:
                while True:
                    buf = fh.read(10 << 20)
                    if not buf:
                        break
                    sha.update(buf)
                if sha.hexdigest() != info['sha256']:
                    raise ValidationError(f'{filepath}: Hash mismatch')
        info['format'] = format_
        info['size'] = filepath.stat().st_size

    # Write index.html
    with open(os.path.join(dirpath, 'index.html'), 'w') as fh:
        index_template.stream(
            has_parent=True,
            title=format_,
            files=slides,
            extras=[
                {
                    'name': 'index.yaml',
                    'description': 'Slide metadata',
                    'size': os.stat(yamlpath).st_size,
                },
            ],
        ).dump(fh)

    return format_, slides


def process_repo(basepath, check_hashes=False):
    # Enumerate directory names
    directories = sorted(path for path in basepath.iterdir() if path.is_dir())

    # Descend into directories
    dir_formats = {}
    slides = {}
    for dirpath in directories:
        dir_format, dir_slides = process_dir(
            dirpath, check_hashes=check_hashes
        )
        dirname = str(dirpath.relative_to(basepath))
        dir_formats[dirname] = dir_format
        for filename, info in dir_slides.items():
            slides[f'{dirname}/{filename}'] = info

    # Write index.json
    jsonpath = basepath / 'index.json'
    with open(jsonpath, 'w') as fh:
        json.dump(slides, fh, indent=2, sort_keys=True)

    # Write index.html
    with open(basepath / 'index.html', 'w') as fh:
        index_template.stream(
            title='openslide-testdata',
            dirs=dir_formats,
            extras=[
                {
                    'name': 'index.json',
                    'description': 'Consolidated metadata for all slides',
                    'size': jsonpath.stat().st_size,
                },
            ],
        ).dump(fh)


def _main():
    parser = argparse.ArgumentParser(
        description='Process metadata and build indexes for openslide-testdata.'
    )
    parser.add_argument(
        'path', type=Path, help='path to local copy of openslide-testdata'
    )
    parser.add_argument(
        '-c',
        '--check-hashes',
        action='store_true',
        help='check SHA-256 digests',
    )
    args = parser.parse_args()
    process_repo(args.path, check_hashes=args.check_hashes)


if __name__ == '__main__':
    _main()
