---
title: Generic tiled TIFF format
permalink: /formats/generic-tiff/
redirect_from:
  - /Generic tiled TIFF format/
---

Format
: single-file pyramidal tiled TIFF

File extensions
: `.tif`

OpenSlide vendor backend
: `generic-tiff`


## Detection

OpenSlide will detect a file as generic TIFF if:

 1. No other detections succeed.
 2. The file is TIFF.
 3. The initial image is tiled.


## TIFF Image Directory Organization

The first image in the TIFF file is the full-resolution image. Any
other tiled images in the file with the "reduced resolution" bit set
are assumed to be reduced-resolution versions of the original.

Starting after OpenSlide 4.0.0, OpenSlide supports generic TIFF files with
missing tiles, i.e. tiles with zero bytes of image data.  These tiles are
rendered as transparent pixels.


## ICC Profiles

The slide ICC profile is taken from the `ICC Profile` tag of the
highest-resolution level.


## Associated Images

None.


## Known Properties

Many TIFF tags are encoded as properties starting with "`tiff.`".


## Test Data

<https://openslide.cs.cmu.edu/download/openslide-testdata/Generic-TIFF/>
