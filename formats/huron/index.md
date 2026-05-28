---
title: Huron format
permalink: /formats/huron/
---

{% include links.md %}

Format
: single-file pyramidal tiled TIFF with non-standard metadata

File extensions
: `.tif`

OpenSlide vendor backend
: `huron`


## Detection

Huron slides are stored in single-file TIFF format. OpenSlide will detect a
file as Huron if:

 1. The file is TIFF.
 2. The initial image is tiled.
 3. The `ImageMake` tag starts with `Huron`.


## Relevant TIFF tags

Tag                 | Description                    |
--------------------|--------------------------------|
`ImageDescription`|Stores some important key-value pairs, see below|
`ImageMake`|Starts with `Huron`|
`NewSubfileType`|1 for the label associated image, 9 for the macro associated image|
`XResolution`, `YResolution`, `ResolutionUnit`|The pixel size in pyramid level 0|


## Extra data stored in `ImageDescription`

The `ImageDescription` tag of the first TIFF directory contains
newline-delimited key-value pairs. A key-value pair is equals-delimited
with extra padding spaces. These key-values are stored as properties
starting with "`huron.`". Currently, OpenSlide does not use any of the
information present in these key-value fields.


## TIFF Image Directory Organization

The directory organization follows the same pattern as the
[Aperio format][format-aperio].


## Associated Images

There are up to three stripped images: a thumbnail image, which is
always the second image in the file; and label and macro images at the
end of the file, with subfile types 1 and 9 respectively.

`label`
: optional, non-tiled image with subfile type 1

`macro`
: optional, non-tiled image with subfile type 9

`thumbnail`
: the second image in the file


## Known Properties

All key-value data encoded in the `ImageDescription` TIFF field is
represented as properties prefixed with "`huron.`".

`openslide.mpp-x`
: normalized TIFF resolution

`openslide.mpp-y`
: normalized TIFF resolution


## Test Data

<https://openslide.cs.cmu.edu/download/openslide-testdata/Huron/>
