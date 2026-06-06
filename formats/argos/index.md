---
title: ARGOS format
permalink: /formats/argos/
---

Format
: single-file pyramidal tiled BigTIFF with non-standard metadata

File extensions
: `.avs`

OpenSlide vendor backend
: `argos`


## Vendor Documentation

[Documentation PDF](https://github.com/user-attachments/files/15580286/ARGOS.AVS.File.Format.pdf)


## Detection

ARGOS slides are stored in single-file BigTIFF format.  OpenSlide will detect
a file as ARGOS if:

 1. The file is TIFF.
 2. The initial image is tiled.
 3. Tag 65000 contains valid XML whose root element is  `Argos.Scan.Metadata`.


## Relevant TIFF tags

Tag                 | Description                    |
--------------------|--------------------------------|
65000               | Metadata XML                   |


## Metadata XML

The first TIFF directory includes metadata XML in TIFF tag 65000.  The
field type is ASCII, but in our samples the value is not NUL-terminated
as required by TIFF, causing libtiff to warn about it.

Value               | Description                    |
--------------------|--------------------------------|
`MaxZ`              | Integer identifier for highest focal plane |
`MinZ`              | Integer identifier for lowest focal plane |
`ScanArea`          | Coordinates of scanned portion of the slide (cm) |
`ZRange`            | Distance between outermost focal planes (μm) |


## TIFF Image Directory Organization

The TIFF file contains the image pyramid of the lowest focal plane,
followed by each higher plane in succession.  Images are sparse, with
missing tiles represented by a zero `TileOffset` and a zero `TileByteCount`.

The last two TIFF directories are the thumbnail and macro images, which are
both stripped.


## Associated Images

`thumbnail`
: second-to-last image in the file, non-tiled

`macro`
: last image in the file, non-tiled


## Known Properties

All simple key-value data encoded in the metadata XML is represented as
properties prefixed with "`argos.`".

`openslide.barcode`
: `argos.Barcode`

`openslide.mpp-x`
: calculated as `10000/tiff.XResolution`, if `tiff.ResolutionUnit` is
`centimeter`

`openslide.mpp-y`
: calculated as `10000/tiff.YResolution`, if `tiff.ResolutionUnit` is
`centimeter`

`openslide.objective-power`
: normalized `argos.ObjectiveMagnification`


## Test Data

<https://openslide.cs.cmu.edu/download/openslide-testdata/Argos/>
