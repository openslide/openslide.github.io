---
layout: default
title: Trestle format
---

Format
:single-file pyramidal tiled TIFF, with non-standard metadata and overlaps; additional files can contain more metadata and detailed overlap info

File extensions
: `.tif`

OpenSlide vendor backend
: `trestle`

OpenSlide ops backend
: `tiff`


Detection
---------

Trestle slides are stored in single-file TIFF format. OpenSlide will detect a file as Trestle if:

 1. The file is TIFF.
 2. The TIFF `Software` tag starts with "`MedScan`".
 3. The `ImageDescription` tag is present.


Relevant TIFF tags
------------------

Tag                         | Description                                    |
----------------------------|------------------------------------------------|
`ImageDescription`          |Stores some important key-value pairs, see below|
`Software`                  |Starts with "`MedScan`"                         |
`XResolution`, `YResolution`|Seems to store microns-per-pixel (MPP), which may or may not take into account the correct objective power. Note that this is inverted from standard TIFF, which stores pixels-per-unit, not units-per-pixel.|


Extra data stored in `ImageDescription`
---------------------------------------

The `ImageDescription` tag contains semicolon-delimited key-value
pairs. A key-value pair is equals-delimited. We use the `OverlapsXY`
and `Background Color` keys from the `ImageDescription`, and ignore
the rest. All of these values are stored as properties starting with
"`trestle.`".

Key              | Description                              |
-----------------|------------------------------------------|
`Background Color`|Hex-encoded background color info, assumed to be in the format `RRGGBB`.|
`White Balance`|Hex-encoded white balance|
`Objective Power`|Reported objective power, often incorrect.|
`JPEG Quality`|The JPEG quality value.|
`OverlapsXY`|Overlaps, see below.|

TIFF Image Directory Organization
---------------------------------

The first image in the TIFF file is the full-resolution image. The
subsequent images are assumed to be decreasingly sized
reduced-resolution images.


Overlaps
--------

The `OverlapsXY` pseudo-field encodes a list of tile overlap values as
ASCII.

Example: "` 64 64 32 32 16 16`" (note the initial space).

These values are assumed to represent the amount of overlap between
adjacent tiles in pixels, in both X and Y. This example encodes 3
levels worth of overlaps. Further overlaps are assumed to have the
value 0.


Associated Images
-----------------

None.


Known Properties
----------------

All data encoded in the `ImageDescription` TIFF field is represented
as properties prefixed with "`trestle.`".

Test Data
---------

<http://openslide.cs.cmu.edu/download/openslide-testdata/Trestle/>
