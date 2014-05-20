---
layout: default
title: Trestle format
permalink: /formats/trestle/
redirect_from:
  - /Trestle format/
---

Format
: single-file pyramidal tiled TIFF, with non-standard metadata and overlaps; additional files contain more metadata and detailed overlap info

File extensions
: `.tif`

OpenSlide vendor backend
: `trestle`


Detection
---------

Trestle slides are stored in single-file TIFF format. OpenSlide will detect a file as Trestle if:

 1. The file is TIFF.
 2. The TIFF `Software` tag starts with `MedScan`.
 3. The `ImageDescription` tag is present.
 4. All images are tiled.


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

These values represent the standard overlaps between adjacent tiles in
X and Y, in pixels. This example encodes 3 levels worth of overlaps.
Further overlaps are assumed to have the value 0.

Individual tile overlaps may differ from the standard overlaps.  These
individual overlaps are recorded in `.tif-Nb` files adjacent to the `.tif`
file, where `N` is the level number.  OpenSlide does not read these files,
though they have been partially decoded; see [issue 21][overlap-files] for
details.

[overlap-files]: https://github.com/openslide/openslide/issues/21#issuecomment-23615583


Associated Images
-----------------

macro
: the image with a filename extension of "`.Full`" (optional)


Known Properties
----------------

All data encoded in the `ImageDescription` TIFF field is represented
as properties prefixed with "`trestle.`".

`openslide.mpp-x`
: copy of `tiff.XResolution` (note that this is a totally non-standard use
of this TIFF tag)

`openslide.mpp-y`
: copy of `tiff.YResolution` (note that this is a totally non-standard use
of this TIFF tag)

`openslide.objective-power`
: normalized `trestle.Objective Power`


Test Data
---------

<http://openslide.cs.cmu.edu/download/openslide-testdata/Trestle/>
