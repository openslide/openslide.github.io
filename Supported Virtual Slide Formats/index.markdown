---
layout: default
title: Virtual slide formats understood by OpenSlide
---

Trestle
-------
Single-file pyramidal tiled TIFF, with non-standard metadata and
overlaps. Additional files can contain more metadata and detailed
overlap info.

File extensions
:`.tif`

OpenSlide vendor backend
:`trestle`

OpenSlide ops backend
:`tiff`

More info
:[Trestle format][1]

[1]: /Trestle%20format


Hamamatsu
---------

Multi-file JPEG/NGR with proprietary metadata and index file formats.

File extensions
:`.vms`, `.vmu`

OpenSlide vendor backend
:`hamamatsu`

OpenSlide ops backend
:`jpeg` for `.vms`, `ngr` for `.vmu`

More info
:[Hamamatsu format][2]

[2]: /Hamamatsu%20format


Aperio
------

Single-file pyramidal tiled TIFF, with non-standard metadata and compression.

File extensions
:`.svs`, `.tif`

OpenSlide vendor backend
:`aperio`

OpenSlide ops backend
:`tiff`

More info
:[Aperio format][3]

[3]: /Aperio%20format


MIRAX
-----

Multi-file JPEG with very complicated proprietary metadata and indexes.

File extensions
:`.mrxs`

OpenSlide vendor backend
:`mirax`

OpenSlide ops backend
:`jpeg`

More info
:[MIRAX format][4]

[4]: /MIRAX%20format


Generic tiled TIFF
------------------

Single-file pyramidal tiled TIFF.

File extensions
:`.tif`

OpenSlide vendor backend
:`generic-tiff`

OpenSlide ops backend
:`tiff`

More info
:[Generic tiled TIFF format][5]

[5]: /Generic%20tiled%20TIFF%20format
