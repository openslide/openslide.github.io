---
layout: default
title: MIRAX format
---

Format
:multi-file JPEG with very complicated proprietary metadata and indexes

File extensions
:`.mrxs`

OpenSlide vendor backend
:`mirax`

OpenSlide ops backend
:`jpeg`


Detection
---------
**Note: MIRAX is incredibly complicated. These detection steps are probably not complete.**


OpenSlide will detect a file as MIRAX if:

 1. The file ends with `.mrxs`.
 2. A directory exists in the same location as the file, with the same name as the file minus the extension.
 3. A file named `Slidedat.ini` exists in the directory.
 4. The slidedat file is readable as a Windows INI-style file.
 5. The slidedat file has a `[GENERAL]` section with the following keys: `SLIDE_VERSION`, `SLIDE_ID`, `IMAGENUMBER_X`, `IMAGENUMBER_Y`.
 6. The slidedat file has a `[HIERARCHICAL]` section with the following keys: `HIER_COUNT`, `NONHIER_COUNT`, `INDEXFILE`.
 7. A key exists in the `[HIERARCHICAL]` section with the value of `Slide zoom level`. The key matches this printf-style template: `HIER_%d_NAME`. The `%d` is bound to the variable `zoom_level`. Currently, `zoom_level` must be 0.
 8. The `[HIERARCHICAL]` section has a key with the name `HIER_%d_COUNT` where `%d` is the value of `zoom_level` in the previous step. The value must be an integer, interpreted as `zoom_count`.
 9. Setting `x` to `zoom_level` and `y` from 0 to `zoom_count`, the `[HIERARCHICAL]` section has a key with the name `HIER_x_VAL_y_SECTION`. Let `section_names[]` be an array of length zoom_count, holding the values for each key.
 10. The `[DATAFILE]` section must exist, with the following keys: `FILE_COUNT`.
 11. There are `FILE_COUNT` keys in the `[DATAFILE]` section with the following names: `FILE_%d`, where `%d` goes from 0 to `FILE_COUNT-1`.
 12. For each value in `section_names`, a group must exist with that name. Each group must contain the keys: `OVERLAP_X`, `OVERLAP_Y`, `IMAGE_FILL_COLOR_BGR`, `DIGITIZER_WIDTH`, `DIGITIZER_HEIGHT`, `IMAGE_CONCAT_FACTOR`. The overlap values must be parseable as doubles, the rest as integers. The key `IMAGE_FORMAT` must exist, with the value `JPEG`.
 13. The `[HIERARCHICAL]` section has a key with the name `NONHIER_%d_NAME` (`%d` is an integer) and with the value `Scan data layer`. Bind `%d` to the variable `scan_nonhier_offset`.
 14. The `[HIERARCHICAL]` section has a key with the name `NONHIER_%d_VAL_%d` where the first `%d` is the value of `scan_nonhier_offset`. The key has a value of `ScanDataLayer_SlideThumbnail`.
 15. The `[HIERARCHICAL]` section has a key with the name `NONHIER_%d_VAL_%d` where the first `%d` is the value of `scan_nonhier_offset`. The key has a value of `ScanDataLayer_SlideBarcode`.
 16. The `[HIERARCHICAL]` section has a key with the name `NONHIER_%d_VAL_%d` where the first `%d` is the value of `scan_nonhier_offset`. The key has a value of `ScanDataLayer_SlidePreview`.
 17. The value of the `INDEXFILE` key above is the name of a readable file.
 18. The index file is of a valid format, and all data referred to by it is valid (see below).


Overview
--------

Because JPEG does not allow for large files, multiple JPEG files are
needed to encode large images.

Unfortunately, (unlike TIFF) JPEG provides very poor support for
random-access decoding of parts of a file. To avoid having many
individual files, MIRAX packs JPEG files into a small number of data
files. The index file provides offsets into the data files for each
required piece of data.

The camera on MIRAX scanners takes overlapping photos and records the
position of each one.  Each photo is then split into multiple JPEG tiles
which do not overlap.  Overlaps only occur between tiles that come
from different photos.

To generate level `n + 1`, each JPEG tile from level `n` is downsampled by
2 and then concatenated into a new JPEG tile, 4 old tiles per new JPEG
tile (2 x 2).  This process is repeated for each level, irrespective of
tile overlaps.  Therefore, at sufficiently high levels, a single tile can
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
data items consisting of a tile index, offset and length within a file, and
a file number.  The file number can be converted to a data file name via the
`DATAFILE` slidedat section.  The tile index is equal to `tile_y *
GENERAL.IMAGENUMBER_X + tile_x`.  Tile coordinates which are not multiples
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
one entry for each camera position (*not* each tile position) in row-major
order.  Each entry is nine bytes: a flag byte, the `X` pixel coordinate of
the photo (4 bytes, little-endian), and the `Y` coordinate (4 bytes,
little-endian).

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
[Introduction to MIRAX/MRXS][1]

[1]: http://lists.andrew.cmu.edu/pipermail/openslide-users/2012-July/000373.html


Test Data
---------
<http://openslide.cs.cmu.edu/download/openslide-testdata/Mirax/>
