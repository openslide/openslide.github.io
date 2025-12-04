#!/usr/bin/env python3
#
# _synctiles - Generate and upload Deep Zoom tiles for test slides
#
# Copyright (c) 2010-2015 Carnegie Mellon University
# Copyright (c) 2016-2025 Benjamin Gilbert
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

from argparse import ArgumentParser, FileType
import base64
from collections.abc import Callable, Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from hashlib import md5, sha256
from io import BytesIO
import json
import os
from pathlib import Path, PurePath
import re
import sys
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any, NotRequired, Self, TextIO, TypedDict
from unicodedata import normalize
from urllib.parse import urljoin
from zipfile import ZipFile
import zlib

from PIL import ImageCms
from PIL.Image import Image
from PIL.ImageCms import ImageCmsProfile
import boto3
import openslide
from openslide import (
    AbstractSlide,
    ImageSlide,
    OpenSlide,
    OpenSlideCache,
    OpenSlideError,
)
from openslide.deepzoom import DeepZoomGenerator
import requests

if TYPE_CHECKING:
    from mypy_boto3_s3.service_resource import Object

STAMP_VERSION = 'threads'  # change to retile without OpenSlide version bump
CORS_ORIGINS = ['*']
DOWNLOAD_BASE_URL = 'https://openslide.cs.cmu.edu/download/openslide-testdata/'
DOWNLOAD_INDEX = 'index.json'
VIEWER_SLIDE_NAME = 'slide'
METADATA_NAME = 'info.json'
STATUS_NAME = 'status.json'
SLIDE_PROPERTIES_NAME = 'properties.json'
SLIDE_METADATA_NAME = 'slide.json'
FORMAT = 'jpeg'
QUALITY = 75
TILE_SIZE = 510
OVERLAP = 1
LIMIT_BOUNDS = True
GROUP_NAME_MAP = {
    'Generic-TIFF': 'Generic TIFF',
    'Hamamatsu': 'Hamamatsu NDPI',
    'Hamamatsu-vms': 'Hamamatsu VMS',
    'Mirax': 'MIRAX',
    'Philips-TIFF': 'Philips TIFF',
}
BUCKET_STATIC = {
    PurePath('robots.txt'): {
        'data': 'User-agent: *\nDisallow: /\n',
        'content-type': 'text/plain',
    },
}
CACHE_CONTROL_NOCACHE = 'no-cache'
CACHE_CONTROL_CACHE = 'public, max-age=31536000'

# Optimized sRGB v2 profile, CC0-1.0 license
# https://github.com/saucecontrol/Compact-ICC-Profiles/blob/bdd84663/profiles/sRGB-v2-micro.icc
# ImageCms.createProfile() generates a v4 profile and Firefox has problems
# with those: https://littlecms.com/blog/2020/09/09/browser-check/
SRGB_PROFILE_BYTES = zlib.decompress(
    base64.b64decode(
        'eNpjYGA8kZOcW8wkwMCQm1dSFOTupBARGaXA/oiBmUGEgZOBj0E2Mbm4wDfYLYQBCIoT'
        'y4uTS4pyGFDAt2sMjCD6sm5GYl7K3IkMtg4NG2wdSnQa5y1V6mPADzhTUouTgfQHII5P'
        'LigqYWBg5AGyecpLCkBsCSBbpAjoKCBbB8ROh7AdQOwkCDsErCYkyBnIzgCyE9KR2ElI'
        'bKhdIMBaCvQsskNKUitKQLSzswEDKAwgop9DwH5jFDuJEMtfwMBg8YmBgbkfIZY0jYFh'
        'eycDg8QthJgKUB1/KwPDtiPJpUVlUGu0gLiG4QfjHKZS5maWk2x+HEJcEjxJfF8Ez4t8'
        'k8iS0VNwVlmjmaVXZ/zacrP9NbdwX7OQshjxFNmcttKwut4OnUlmc1Yv79l0e9/MU8ev'
        'pz4p//jz/38AR4Nk5Q=='
    )
)
SRGB_PROFILE: ImageCmsProfile = ImageCms.getOpenProfile(
    BytesIO(SRGB_PROFILE_BYTES)
)  # type: ignore[no-untyped-call]

KeyMd5s = dict[PurePath, str]
TestDataIndex = dict[str, 'TestDataSlide']


class TestDataSlide(TypedDict):
    """One openslide-testdata slide from index.json."""

    credit: NotRequired[str]
    description: str
    format: str
    license: str
    sha256: str
    size: int


class Context(TypedDict):
    """Cross-stage context JSON."""

    openslide: str
    openslide_python: str
    stamp: str
    slides: TestDataIndex
    bucket: str


class Matrix(TypedDict):
    """Job matrix for GitHub Actions."""

    slide: list[str]


class SlideMetadata(TypedDict):
    """Per-slide slide.json stored in the bucket and used by this script."""

    name: str
    stamp: str
    slide: NotRequired[ImageInfo]
    associated: NotRequired[list[ImageInfo]]
    properties: NotRequired[dict[str, str]]
    properties_url: NotRequired[str]


class BucketMetadata(TypedDict):
    """Bucket info.json, for the frontend."""

    openslide: str
    openslide_python: str
    stamp: str
    groups: list[SlideGroup]


class SlideGroup(TypedDict):
    name: str
    slides: list[SlideSummary]


class SlideSummary(TypedDict):
    name: str
    slide: ImageInfo
    associated: list[ImageInfo]
    properties_url: str
    credit: str | None
    description: str
    download_url: str


class ImageInfo(TypedDict):
    name: str | None
    mpp: float | None
    source: DzSource


class DzSource(TypedDict):
    Image: DzSourceImage


class DzSourceImage(TypedDict):
    xmlns: str
    Url: str
    Format: str
    TileSize: int
    Overlap: int
    Size: DzSourceImageSize


class DzSourceImageSize(TypedDict):
    Width: int
    Height: int


class StatusMetadata(TypedDict):
    """status.json object for the frontend."""

    dirty: bool
    stamp: str | None


def slugify(text: str) -> str:
    """Generate an ASCII-only slug."""
    text = normalize('NFKD', text.lower()).encode('ascii', 'ignore').decode()
    return re.sub('[^a-z0-9]+', '_', text)


class Generator:
    def __init__(self, slide: AbstractSlide):
        self.dz = DeepZoomGenerator(
            slide, TILE_SIZE, OVERLAP, limit_bounds=LIMIT_BOUNDS
        )
        self._transform = self._get_transform(slide)

    @staticmethod
    def _get_transform(image: AbstractSlide) -> Callable[[Image], None]:
        """Return a function that transforms an image to sRGB in place."""
        if image.color_profile is None:
            return lambda img: None
        intent: int = ImageCms.getDefaultIntent(
            image.color_profile
        )  # type: ignore[no-untyped-call]
        transform = ImageCms.buildTransform(
            image.color_profile, SRGB_PROFILE, 'RGB', 'RGB', intent, 0
        )

        def xfrm(img: Image) -> None:
            ImageCms.applyTransform(img, transform, True)
            # Some browsers assume we intend the display's color space if we
            # don't embed the profile.  Pillow's serialization is larger, so
            # use ours.
            img.info['icc_profile'] = SRGB_PROFILE_BYTES

        return xfrm

    def get_tile(self, level: int, address: tuple[int, int]) -> Image:
        tile: Image = self.dz.get_tile(level, address)
        self._transform(tile)
        return tile


class S3Storage:
    def __init__(self, bucket_name: str) -> None:
        self.conn = boto3.resource('s3')
        self.bucket = self.conn.Bucket(bucket_name)
        region = self.conn.meta.client.head_bucket(Bucket=bucket_name)[
            'ResponseMetadata'
        ]['HTTPHeaders']['x-amz-bucket-region']
        self.base_url = (
            f'https://{bucket_name}.s3.dualstack.{region}.amazonaws.com/'
        )
        self.NoSuchKey = self.conn.meta.client.exceptions.NoSuchKey

    def object(self, path: PurePath) -> Object:
        return self.bucket.Object(path.as_posix())

    def upload_metadata(
        self, path: PurePath, item: Any, cache: bool = True
    ) -> None:
        self.object(path).put(
            Body=json.dumps(item, indent=1, sort_keys=True).encode(),
            CacheControl=(
                CACHE_CONTROL_CACHE if cache else CACHE_CONTROL_NOCACHE
            ),
            ContentType='application/json',
        )


@dataclass
class Tile:
    storage: S3Storage
    generator: Generator
    level: int
    address: tuple[int, int]
    key_name: PurePath
    cur_md5: str | None

    def sync(self) -> PurePath:
        """Generate and possibly upload a tile."""
        tile = self.generator.get_tile(self.level, self.address)
        buf = BytesIO()
        tile.save(
            buf,
            FORMAT,
            quality=QUALITY,
            icc_profile=tile.info.get('icc_profile'),
        )
        new_md5 = md5(buf.getbuffer())
        if self.cur_md5 != new_md5.hexdigest():
            self.storage.object(self.key_name).put(
                Body=buf.getvalue(),
                CacheControl=CACHE_CONTROL_CACHE,
                ContentMD5=base64.b64encode(new_md5.digest()).decode(),
                ContentType=f'image/{FORMAT}',
            )
        return self.key_name

    @classmethod
    def enumerate(
        cls,
        storage: S3Storage,
        generator: Generator,
        key_imagepath: PurePath,
        key_md5sums: KeyMd5s,
    ) -> Iterator[Self]:
        """Enumerate tiles in a single image."""
        for level in range(generator.dz.level_count):
            key_levelpath = key_imagepath / str(level)
            cols, rows = generator.dz.level_tiles[level]
            for row in range(rows):
                for col in range(cols):
                    key_name = key_levelpath / f'{col}_{row}.{FORMAT}'
                    yield cls(
                        storage,
                        generator,
                        level,
                        (col, row),
                        key_name,
                        key_md5sums.get(key_name),
                    )


def sync_image(
    exec: ThreadPoolExecutor,
    storage: S3Storage,
    generator: Generator,
    slide_relpath: PurePath,
    associated: str | None,
    key_basepath: PurePath,
    key_md5sums: KeyMd5s,
    mpp: float | None = None,
) -> ImageInfo:
    """Generate and upload tiles, and generate metadata, for a single image.
    Delete valid tiles from key_md5sums."""

    count = 0
    total = generator.dz.tile_count
    associated_slug = slugify(associated) if associated else VIEWER_SLIDE_NAME
    key_imagepath = key_basepath / f'{associated_slug}_files'

    def progress() -> None:
        print(
            f"Tiling {slide_relpath} {associated_slug}: "
            f"{count}/{total} tiles\r",
            end='',
        )
        sys.stdout.flush()

    # Sync tiles
    progress()
    for future in as_completed(
        exec.submit(Tile.sync, tile)
        for tile in Tile.enumerate(
            storage, generator, key_imagepath, key_md5sums
        )
    ):
        key_md5sums.pop(future.result(), None)
        count += 1
        if count % 100 == 0:
            progress()
    progress()
    print()

    # Format tile source
    source: DzSource = {
        'Image': {
            'xmlns': 'http://schemas.microsoft.com/deepzoom/2008',
            'Url': urljoin(storage.base_url, key_imagepath.as_posix()) + '/',
            'Format': FORMAT,
            'TileSize': TILE_SIZE,
            'Overlap': OVERLAP,
            'Size': {
                'Width': generator.dz.level_dimensions[-1][0],
                'Height': generator.dz.level_dimensions[-1][1],
            },
        }
    }

    # Return metadata
    return {
        'name': associated,
        'mpp': mpp,
        'source': source,
    }


def sync_slide(
    stamp: str,
    storage: S3Storage,
    slide_relpath: PurePath,
    slide_info: TestDataSlide,
    workers: int,
) -> SlideMetadata:
    """Generate and upload tiles and metadata for a single slide."""

    key_basepath = PurePath(slide_relpath.with_suffix('').as_posix().lower())
    metadata_key_name = key_basepath / SLIDE_METADATA_NAME
    properties_key_name = key_basepath / SLIDE_PROPERTIES_NAME

    # Get current metadata
    try:
        metadata: SlideMetadata | None = json.load(
            storage.object(metadata_key_name).get()['Body']
        )
    except storage.NoSuchKey:
        metadata = None

    # Return if metadata is current
    if metadata is not None and metadata['stamp'] == stamp:
        return metadata

    with TemporaryDirectory(prefix='synctiles-', dir='/var/tmp') as td:
        tempdir = Path(td)

        # Fetch slide
        print(f'Fetching {slide_relpath}...')
        count = 0
        hash = sha256()
        slide_path = tempdir / slide_relpath.name
        with slide_path.open('wb') as fh:
            r = requests.get(
                urljoin(DOWNLOAD_BASE_URL, slide_relpath.as_posix()),
                stream=True,
            )
            r.raise_for_status()
            for buf in r.iter_content(10 << 20):
                if not buf:
                    break
                fh.write(buf)
                hash.update(buf)
                count += len(buf)
        if count != int(r.headers['Content-Length']):
            raise OSError(f'Short read fetching {slide_relpath}')
        if hash.hexdigest() != slide_info['sha256']:
            raise OSError(f'Hash mismatch fetching {slide_relpath}')

        # Open slide
        slide = None
        try:
            slide = OpenSlide(slide_path)
        except OpenSlideError:
            if slide_relpath.suffix == '.zip':
                # Unzip slide
                print(f'Extracting {slide_relpath}...')
                temp_path = Path(
                    TemporaryDirectory(dir=tempdir, delete=False).name
                )
                with ZipFile(slide_path) as zf:
                    zf.extractall(path=temp_path)
                # Find slide in zip
                for slide_path in temp_path.iterdir():
                    try:
                        slide = OpenSlide(slide_path)
                    except OpenSlideError:
                        pass
                    else:
                        break
        # slide will be None if we can't read it

        # Enumerate existing keys
        print(f"Enumerating keys for {slide_relpath}...")
        key_md5sums = {}
        for obj in storage.bucket.objects.filter(
            Prefix=key_basepath.as_posix() + '/'
        ):
            key_md5sums[PurePath(obj.key)] = obj.e_tag.strip('"')

        # Initialize metadata
        metadata = {
            'name': slide_relpath.stem,
            'stamp': stamp,
        }

        if slide is not None:
            # Configure cache
            slide.set_cache(OpenSlideCache(workers << 25))

            # Add slide metadata
            metadata.update(
                {
                    'associated': [],
                    'properties': dict(slide.properties),
                    'properties_url': urljoin(
                        storage.base_url, properties_key_name.as_posix()
                    )
                    + '?v='
                    + stamp,
                }
            )

            # Calculate microns per pixel
            try:
                mpp_x = slide.properties[openslide.PROPERTY_NAME_MPP_X]
                mpp_y = slide.properties[openslide.PROPERTY_NAME_MPP_Y]
                mpp = (float(mpp_x) + float(mpp_y)) / 2
            except (KeyError, ValueError):
                mpp = None

            # Start compute pool
            exec = ThreadPoolExecutor(workers)
            try:
                # Tile slide
                def do_tile(
                    associated: str | None, image: AbstractSlide
                ) -> ImageInfo:
                    return sync_image(
                        exec,
                        storage,
                        Generator(image),
                        slide_relpath,
                        associated,
                        key_basepath,
                        key_md5sums,
                        mpp if associated is None else None,
                    )

                metadata['slide'] = do_tile(None, slide)

                # Tile associated images
                for associated, image in sorted(
                    slide.associated_images.items()
                ):
                    cur_props = do_tile(associated, ImageSlide(image))
                    metadata['associated'].append(cur_props)
            except BaseException:
                exec.shutdown(cancel_futures=True)
                raise
            finally:
                exec.shutdown()

    # Delete old keys
    for name in metadata_key_name, properties_key_name:
        key_md5sums.pop(name, None)
    if key_md5sums:
        to_delete = [k for k in key_md5sums]
        print(f"Pruning {len(to_delete)} keys for {slide_relpath}...")
        while to_delete:
            cur_delete, to_delete = to_delete[0:1000], to_delete[1000:]
            delete_result = storage.bucket.delete_objects(
                Delete={
                    'Objects': [{'Key': k.as_posix()} for k in cur_delete],
                    'Quiet': True,
                },
            )
            if 'Errors' in delete_result:
                raise OSError(
                    f'Failed to delete {len(delete_result["Errors"])} keys'
                )

    # Update metadata
    if 'properties' in metadata:
        storage.upload_metadata(properties_key_name, metadata['properties'])
    storage.upload_metadata(metadata_key_name, metadata, cache=False)

    return metadata


def upload_status(
    storage: S3Storage, dirty: bool = False, stamp: str | None = None
) -> None:
    status: StatusMetadata = {
        'dirty': dirty,
        'stamp': stamp,
    }
    storage.upload_metadata(PurePath(STATUS_NAME), status, False)


def start_retile(
    bucket_name: str, ctxfile: TextIO, matrixfile: TextIO
) -> None:
    """Subcommand to initialize a retiling run.  Writes common state into
    ctxfile and a list of slides to be retiled into matrixfile."""

    # Get openslide-testdata index
    r = requests.get(urljoin(DOWNLOAD_BASE_URL, DOWNLOAD_INDEX))
    r.raise_for_status()
    slides: TestDataIndex = r.json()

    # Initialize context for the run
    context: Context = {
        'openslide': openslide.__library_version__,
        'openslide_python': openslide.__version__,
        'stamp': sha256(
            (
                f'{openslide.__library_version__} {openslide.__version__} '
                f'{STAMP_VERSION}'
            ).encode()
        ).hexdigest()[:8],
        'slides': slides,
        'bucket': bucket_name,
    }
    print(
        f'OpenSlide {context["openslide"]}, '
        f'OpenSlide Python {context["openslide_python"]}'
    )

    # Connect to S3
    storage = S3Storage(bucket_name)

    # Set bucket configuration
    print("Configuring bucket...")
    storage.bucket.Cors().put(
        CORSConfiguration={
            'CORSRules': [
                {
                    'AllowedMethods': ['GET'],
                    'AllowedOrigins': CORS_ORIGINS,
                },
            ],
        }
    )

    # Store static files
    print("Storing static files...")
    for relpath, opts in BUCKET_STATIC.items():
        storage.object(relpath).put(
            Body=opts.get('data', '').encode(),
            ContentType=opts['content-type'],
        )

    # If the stamp is changing, mark bucket dirty
    try:
        stream = storage.object(PurePath(METADATA_NAME)).get()['Body']
        metadata: BucketMetadata = json.load(stream)
        old_stamp = metadata['stamp']
    except storage.NoSuchKey:
        old_stamp = None
    if context['stamp'] != old_stamp:
        print('Marking bucket dirty...')
        upload_status(storage, dirty=True, stamp=old_stamp)

    # Write output files
    with ctxfile:
        json.dump(context, ctxfile)
    with matrixfile:
        matrix: Matrix = {
            "slide": sorted(slides.keys()),
        }
        json.dump(matrix, matrixfile)


def retile_slide(
    ctxfile: TextIO, slide_relpath: PurePath, summarydir: Path, workers: int
) -> None:
    """Subcommand to retile one slide into S3.  Writes summary data into
    summarydir."""

    # Load context
    with ctxfile:
        context: Context = json.load(ctxfile)

    # Connect to S3
    storage = S3Storage(context['bucket'])

    # Tile slide
    slide_info = context['slides'].get(slide_relpath.as_posix())
    if slide_info is None:
        raise Exception(f'No such slide {slide_relpath}')
    metadata = sync_slide(
        context['stamp'], storage, slide_relpath, slide_info, workers
    )

    # Write summary if the slide was readable
    if 'slide' in metadata:
        summary: SlideSummary = {
            'name': metadata['name'],
            'slide': metadata['slide'],
            'associated': metadata['associated'],
            'properties_url': metadata['properties_url'],
            'credit': slide_info.get('credit'),
            'description': slide_info['description'],
            'download_url': urljoin(
                DOWNLOAD_BASE_URL, slide_relpath.as_posix()
            ),
        }
        summaryfile = summarydir / slide_relpath
        summaryfile.parent.mkdir(parents=True, exist_ok=True)
        with summaryfile.open('w') as fh:
            json.dump(summary, fh)


def finish_retile(ctxfile: TextIO, summarydir: Path) -> None:
    """Subcommand to finish a retiling run.  Reads context file and summary
    dir and writes metadata to S3."""

    # Load context
    with ctxfile:
        context: Context = json.load(ctxfile)

    # Connect to S3
    storage = S3Storage(context['bucket'])

    # Build group list
    groups: list[SlideGroup] = []
    cur_group_name = None
    cur_slides: list[SlideSummary] = []
    for slide_relpath in sorted(PurePath(p) for p in context['slides']):
        summaryfile = summarydir / slide_relpath
        if summaryfile.exists():
            with summaryfile.open() as fh:
                summary: SlideSummary = json.load(fh)
            group_name = slide_relpath.parent.as_posix()
            if group_name != cur_group_name:
                cur_group_name = group_name
                cur_slides = []
                groups.append(
                    {
                        'name': GROUP_NAME_MAP.get(group_name, group_name),
                        'slides': cur_slides,
                    }
                )
            cur_slides.append(summary)

    # Upload metadata
    print('Storing metadata...')
    metadata: BucketMetadata = {
        'openslide': context['openslide'],
        'openslide_python': context['openslide_python'],
        'stamp': context['stamp'],
        'groups': groups,
    }
    storage.upload_metadata(PurePath(METADATA_NAME), metadata, False)

    # Mark bucket clean
    print('Marking bucket clean...')
    upload_status(storage, stamp=context['stamp'])


if __name__ == '__main__':
    thread_count = 2 * os.process_cpu_count()

    parser = ArgumentParser()
    subparsers = parser.add_subparsers(metavar='subcommand', required=True)

    parser_start = subparsers.add_parser('start', help='start a retiling run')
    parser_start.add_argument(
        'bucket',
        help='name of destination S3 bucket',
    )
    parser_start.add_argument(
        'context_file',
        type=FileType('w'),
        help='path to context file (output)',
    )
    parser_start.add_argument(
        'matrix_file',
        type=FileType('w'),
        help='path to list of slides to tile (output)',
    )
    parser_start.set_defaults(cmd='start')

    parser_tile = subparsers.add_parser('tile', help='retile one slide')
    parser_tile.add_argument(
        'context_file', type=FileType('r'), help='path to context file'
    )
    parser_tile.add_argument(
        'slide', type=PurePath, help='slide identifier (from matrix file)'
    )
    parser_tile.add_argument(
        'summary_dir', type=Path, help='path to summary directory (output)'
    )
    parser_tile.add_argument(
        '-j',
        '--jobs',
        metavar='COUNT',
        dest='workers',
        type=int,
        default=thread_count,
        help=f'number of threads to start [{thread_count}]',
    )
    parser_tile.set_defaults(cmd='tile')

    parser_finish = subparsers.add_parser(
        'finish', help='finish a retiling run'
    )
    parser_finish.add_argument(
        'context_file', type=FileType('r'), help='path to context file'
    )
    parser_finish.add_argument(
        'summary_dir', type=Path, help='path to summary directory'
    )
    parser_finish.set_defaults(cmd='finish')

    args = parser.parse_args()
    if args.cmd == 'start':
        start_retile(args.bucket, args.context_file, args.matrix_file)
    elif args.cmd == 'tile':
        retile_slide(
            args.context_file, args.slide, args.summary_dir, args.workers
        )
    elif args.cmd == 'finish':
        finish_retile(args.context_file, args.summary_dir)
    else:
        raise Exception('unimplemented subcommand')
