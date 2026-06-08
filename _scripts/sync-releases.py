#!/usr/bin/env python3
#
# sync-releases - Update release metadata and docs
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

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from io import BytesIO
from pathlib import Path, PurePath
import shutil
from typing import Any
from zipfile import ZipFile

import requests
import yaml


@dataclass
class Project:
    id: str
    repo: str
    docs: Docs | None = None


@dataclass
class Docs:
    workflow: str
    artifact_prefix: str
    subdir: PurePath


TABLES = Path('_data/releases.yaml')
DOCROOT = Path('api')
PROJECTS = (
    Project(
        'c',
        'openslide/openslide',
        Docs('c.yaml', 'openslide-docs-', PurePath()),
    ),
    Project(
        'python',
        'openslide/openslide-python',
        Docs('python.yml', 'openslide-python-docs-', PurePath('python')),
    ),
    Project('java', 'openslide/openslide-java'),
    Project('bin', 'openslide/openslide-bin'),
)


def api_request(endpoint: str) -> Any:
    resp = requests.get(
        f'https://api.github.com/{endpoint}',
        headers={
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2026-03-10',
        },
    )
    resp.raise_for_status()
    return resp.json()


def one(things: Iterable[Any]) -> Any:
    thing_list = list(things)
    assert len(thing_list) == 1, len(thing_list)
    return thing_list[0]


def main() -> None:
    # read release tables
    with TABLES.open() as fh:
        releases = yaml.safe_load(fh)

    # clear docs dir
    if DOCROOT.exists():
        shutil.rmtree(DOCROOT)

    for proj in PROJECTS:
        # get current version from GitHub
        tag = one(api_request(f'repos/{proj.repo}/releases?per_page=1'))[
            'tag_name'
        ]
        assert tag[0] == 'v', tag
        version = tag[1:]

        # add table row for new release
        prev = releases[proj.id][0]
        if version != prev['version']:
            cur = prev.copy()
            cur['version'] = version
            cur['date'] = date.today().strftime('%Y-%m-%d')
            releases[proj.id].insert(0, cur)

        # sync docs
        if proj.docs is not None:
            # find artifact
            url = f'repos/{proj.repo}/actions/workflows/{proj.docs.workflow}/runs?branch={tag}&event=push&status=completed'
            run = one(api_request(url)['workflow_runs'])
            url = f'repos/{proj.repo}/actions/runs/{run["id"]}/artifacts'
            artifact = one(
                a
                for a in api_request(url)['artifacts']
                if a['name'].startswith(proj.docs.artifact_prefix)
            )

            # fetch artifact through third-party service; GitHub wants a
            # token to fetch artifacts.  check hash so we don't have to
            # trust the service
            resp = requests.get(
                f'https://nightly.link/{proj.repo}/actions/artifacts/{artifact["id"]}.zip'
            )
            resp.raise_for_status()
            expected_hash = artifact['digest'].replace('sha256:', '')
            found_hash = sha256(resp.content).hexdigest()
            if expected_hash != found_hash:
                raise Exception(f'SHA-256 {found_hash} != {expected_hash}')

            # unpack
            docdir = DOCROOT / proj.docs.subdir
            docdir.mkdir(parents=True, exist_ok=True)
            ZipFile(BytesIO(resp.content)).extractall(path=docdir)

            # reparent
            wrapper_dir = one(docdir.glob(f'{proj.docs.artifact_prefix}*'))
            for path in wrapper_dir.iterdir():
                path.replace(docdir / path.name)
            wrapper_dir.rmdir()

    # write release tables
    with TABLES.open('w') as fh:
        data = yaml.dump(releases, default_flow_style=None, sort_keys=False)
        # hacks to fix indentation and strip quotes
        data = data.replace('\n-', '\n  -').replace("'", '')
        fh.write(data)


if __name__ == '__main__':
    main()
