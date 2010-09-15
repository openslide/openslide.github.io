---
layout: default
title: Generic tiled TIFF format
---

Format
:single-file pyramidal tiled TIFF

File extensions
:`.tif`

OpenSlide vendor backend
:`generic-tiff`

OpenSlide ops backend
:`tiff`

Detection
---------
OpenSlide will detect a file as generic TIFF if:

 1. No other detections succeed.
 2. The file is TIFF.
 3. The initial image is tiled.

TIFF Image Directory Organization
---------------------------------

The first image in the TIFF file is the full-resolution image. Any
other tiled images in the file with the "reduced resolution" bit set
are assumed to be reduced-resolution versions of the original.

Associated Images
-----------------
None.


Known Properties
----------------

Many TIFF tags are encoded as properties starting with "`tiff.`".