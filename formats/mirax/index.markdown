---
layout: default
title: MIRAX format
---

Format
:multi-file with very complicated proprietary metadata and indexes

File extensions
:`.mrxs`

OpenSlide vendor backend
:`mirax`


Detection
---------

OpenSlide will detect a file as MIRAX if:

 1. The file is not a TIFF.
 2. The filename ends with `.mrxs`.
 3. A directory exists in the same location as the file, with the same name as the file minus the extension.
 4. A file named `Slidedat.ini` exists in the directory.


Overview
--------

MIRAX can store slides in JPEG, PNG, or BMP formats.  Because JPEG does not
allow for large images, and JPEG and PNG provide very poor support for
random-access decoding of part of an image, multiple images are needed to
encode a slide.  To avoid having many individual files, MIRAX packs these
images into a small number of data files.  The index file provides offsets
into the data files for each required piece of data.

The camera on MIRAX scanners takes overlapping photos and records the
position of each one.  Each photo is then split into multiple images
which do not overlap.  Overlaps only occur between images that come
from different photos.

To generate level `n + 1`, each image from level `n` is downsampled by
2 and then concatenated into a new image, 4 old images per new
image (2 x 2).  This process is repeated for each level, irrespective of
image overlaps.  Therefore, at sufficiently high levels, a single image can
contain one or more embedded overlaps of non-integral width.

Index File
----------

The index file starts with a five-character ASCII version string, followed
by the `SLIDE_ID` from the slidedat file.  The rest of the file consists of
32-bit little-endian integers (unaligned), which can be data values or
pointers to byte offsets within the index file.

The first two integers point to offset tables for the hierarchical and
nonhierarchical roots, respectively.  These tables contain one record for
each `VAL` in the `HIERARCHICAL` slidedat section.  For example, the record
for `NONHIER_1_VAL_2` would be stored at `nonhier_root + 4 *
(NONHIER_0_COUNT + 2)`.

Each record is a pointer to a linked list of data pages.  The first two
values in a data page are the number of data items in the page and a pointer
to the next page.  The first page always has 0 data items, and the last page
has a 0 next pointer.

There is one hierarchical record for each zoom level.  The record contains
data items consisting of an image index, offset and length within a file, and
a file number.  The file number can be converted to a data file name via the
`DATAFILE` slidedat section.  The image index is equal to `image_y *
GENERAL.IMAGENUMBER_X + image_x`.  Image coordinates which are not multiples
of the zoom level's downsample factor are omitted.

Nonhierarchical records refer to associated images and additional metadata.
Nonhierarchical data items consist of three zero values followed by an
offset, length, and file number as in hierarchical records.

Data Files
----------

A data file begins with a header containing a five-character ASCII version
string, the `SLIDE_ID` from the slidedat file, the file number encoded into
three ASCII characters, and 256 bytes of padding.  The remainder of the
file contains packed data referenced by the index file.

Slide Position File
-------------------

The slide position file is referenced by the
`VIMSLIDE_POSITION_BUFFER.default` nonhierarchical section.  It contains
one entry for each camera position (*not* each image position) in row-major
order.  Each entry is nine bytes: a flag byte, the `X` pixel coordinate of
the photo (4 bytes, little-endian, may be negative), and the `Y` coordinate
(4 bytes, little-endian, may be negative).  In slides with
`CURRENT_SLIDE_VERSION` &ge; 1.9, the flag byte is 1 if the slide file
contains images for this camera position, 0 otherwise.  In older slides,
the flag byte is always 0.

In slides with `CURRENT_SLIDE_VERSION` &ge; 2.2, the slide position file is
compressed with DEFLATE and referenced by the
`StitchingIntensityLayer.StitchingIntensityLevel` nonhierarchical section.

Associated Images
-----------------

thumbnail
:the image named "`ScanDataLayer_SlidePreview`" in `Slidedat.ini` (optional)

label
:the image named "`ScanDataLayer_SlideBarcode`" in `Slidedat.ini` (optional)

macro
:the image named "`ScanDataLayer_SlideThumbnail`" in `Slidedat.ini` (optional)

Known Properties
----------------

All key-value data stored in the `Slidedat.ini` file are encoded as
properties prefixed with "`mirax.`".

`openslide.mpp-x`
:normalized `MICROMETER_PER_PIXEL_X` from the Slidedat section
corresponding to level 0 (typically
`mirax.LAYER_0_LEVEL_0_SECTION.MICROMETER_PER_PIXEL_X`)

`openslide.mpp-y`
:normalized `MICROMETER_PER_PIXEL_Y` from the Slidedat section
corresponding to level 0 (typically
`mirax.LAYER_0_LEVEL_0_SECTION.MICROMETER_PER_PIXEL_Y`)

`openslide.objective-power`
:normalized `mirax.GENERAL.OBJECTIVE_MAGNIFICATION`


See Also
--------
[Introduction to MIRAX/MRXS][1].  Note that our terminology has changed since
that document was written; where it says "tile", substitute "image", and
where it says "subtile", substitute "tile".

[1]: http://lists.andrew.cmu.edu/pipermail/openslide-users/2012-July/000373.html


Test Data
---------
<http://openslide.cs.cmu.edu/download/openslide-testdata/Mirax/>
