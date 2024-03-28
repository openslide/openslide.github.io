---
title: Aperio format
permalink: /formats/aperio/
redirect_from:
  - /Aperio format/
---

Format
: single-file pyramidal tiled TIFF, with non-standard metadata and compression

File extensions
: `.svs`, `.tif`

OpenSlide vendor backend
: `aperio`


## Vendor Documentation

[Documentation PDF](https://web.archive.org/web/20120420105738/http://www.aperio.com/documents/api/Aperio_Digital_Slides_and_Third-party_data_interchange.pdf)


## Detection

Aperio slides are stored in single-file TIFF format. OpenSlide will detect a file as Aperio if:

 1. The file is TIFF.
 2. The initial image is tiled.
 3. The `ImageDescription` tag starts with `Aperio`.


## Relevant TIFF tags

Tag                 | Description                    |
--------------------|--------------------------------|
`ImageDescription`|Stores some important key-value pairs and other information, see below|
`Compression`|May be 33003 or 33005, which represent specific kinds of JPEG 2000 compression, see below|


## Extra data stored in `ImageDescription`

For tiled images, the `ImageDescription` tag contains some dimensional
downsample information as well as what look like
offsets. Additionally, vertical line-delimited key-value pairs are
stored, in at least the full-resolution image. A key-value pair is
equals-delimited. These key-values are stored as properties starting
with "`aperio.`". Currently, OpenSlide does not use any of the
information present in these key-value fields.

For stripped images, the `ImageDescription` tag may contain a name,
followed by a carriage return. This is used for naming the associated
images. The second image in the file does not have a name, though it
is an associated image.


## TIFF Image Directory Organization

<http://www.aperio.com/documents/api/Aperio_Digital_Slides_and_Third-party_data_interchange.pdf>
page 14:

> The first image in an SVS file is always the baseline image (full
> resolution). This image is always tiled, usually with a tile size
> of 240x240 pixels. The second image is always a thumbnail,
> typically with dimensions of about 1024x768 pixels. Unlike the
> other slide images, the thumbnail image is always
> stripped. Following the thumbnail there may be one or more
> intermediate "pyramid" images. These are always compressed with
> the same type of compression as the baseline image, and have a
> tiled organization with the same tile size.
>
> Optionally at the end of an SVS file there may be a slide label
> image, which is a low resolution picture taken of the slide’s
> label, and/or a macro camera image, which is a low resolution
> picture taken of the entire slide. The label and macro images are
> always stripped.


## JPEG 2000 (compression types 33003 or 33005)

Some Aperio files use compression type 33003 or 33005. Images using
this compression need to be decoded as a JPEG 2000 codestream. For
33003: YCbCr format, possibly with a chroma subsampling of 4:2:2. For
33005: RGB format. Note that the TIFF file may not encode the
colorspace or subsampling parameters in the
`PhotometricInterpretation` field, nor the `YCbCrSubsampling` field,
even though the TIFF standard seems to require this. The correct
subsampling can be found in the JPEG 2000 codestream.


## ICC Profiles

The slide ICC profile is taken from the `ICC Profile` tag of the first
image.


## Associated Images

`label`
: optional, the name "label" is given in `ImageDescription`

`macro`
: optional, the name "macro" is given in `ImageDescription`

`thumbnail`
: the second image in the file


## Known Properties

All key-value data encoded in the `ImageDescription` TIFF field is
represented as properties prefixed with "`aperio.`".

`openslide.mpp-x`
: normalized `aperio.MPP`

`openslide.mpp-y`
: normalized `aperio.MPP`

`openslide.objective-power`
: normalized `aperio.AppMag`


## Test Data

<https://openslide.cs.cmu.edu/download/openslide-testdata/Aperio/>
