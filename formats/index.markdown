---
title: Virtual slide formats understood by OpenSlide
permalink: /formats/
redirect_from:
  - /Supported Virtual Slide Formats/
---

{% include links.markdown %}

OpenSlide's support for these formats is not endorsed by their respective
vendors and may be incomplete.  Problems should be reported to the OpenSlide
[mailing list][users-subscribe] or [issue tracker][c-issues].


Aperio
------

Single-file pyramidal tiled TIFF, with non-standard metadata and compression.

File extensions
: `.svs`, `.tif`

OpenSlide vendor backend
: `aperio`

More info
: [Aperio format][format-aperio]


Hamamatsu
---------

Multi-file JPEG/NGR with proprietary metadata and index file formats, and
single-file TIFF-like format with proprietary metadata.

File extensions
: `.vms`, `.vmu`, `.ndpi`

OpenSlide vendor backend
: `hamamatsu`

More info
: [Hamamatsu format][format-hamamatsu]


Leica
-----

Single-file pyramidal tiled BigTIFF with non-standard metadata.

File extensions
: `.scn`

OpenSlide vendor backend
: `leica`

More info
: [Leica format][format-leica]


MIRAX
-----

Multi-file with very complicated proprietary metadata and indexes.

File extensions
: `.mrxs`

OpenSlide vendor backend
: `mirax`

More info
: [MIRAX format][format-mirax]


Philips
-------

Single-file pyramidal tiled TIFF or BigTIFF with non-standard metadata.

File extensions
: `.tiff`

OpenSlide vendor backend
: `philips`

More info
: [Philips format][format-philips]


Sakura
------
SQLite database containing pyramid tiles and metadata.

File extensions
: `.svslide`

OpenSlide vendor backend
: `sakura`

More info
: [Sakura format][format-sakura]


Trestle
-------
Single-file pyramidal tiled TIFF, with non-standard metadata and
overlaps.  Additional files contain more metadata and detailed overlap info.

File extensions
: `.tif`

OpenSlide vendor backend
: `trestle`

More info
: [Trestle format][format-trestle]


Ventana
-------
Single-file pyramidal tiled BigTIFF, with non-standard metadata and
overlaps.

File extensions
: `.bif`, `.tif`

OpenSlide vendor backend
: `ventana`

More info
: [Ventana format][format-ventana]


Generic tiled TIFF
------------------

Single-file pyramidal tiled TIFF.

File extensions
: `.tif`

OpenSlide vendor backend
: `generic-tiff`

More info
: [Generic tiled TIFF format][format-generic-tiff]
