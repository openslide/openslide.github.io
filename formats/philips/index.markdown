---
title: Philips format
---

{% include links.markdown %}

Format
: single-file pyramidal tiled TIFF or BigTIFF with non-standard metadata

File extensions
: `.tiff`

OpenSlide vendor backend
: `philips`


Detection
---------

Philips TIFF files are stored in single-file TIFF or BigTIFF format.
OpenSlide will detect a file as Philips if:

 1. The file is TIFF.
 2. The TIFF `Software` tag starts with `Philips`.
 3. The `ImageDescription` tag contains valid XML.
 4. The root tag of the XML is `DataObject` and has an `ObjectType` attribute with a value of `DPUfsImport`.

To open BigTIFF files, OpenSlide must be built with libtiff 4 or above.


File Organization
-----------------

Philips TIFF is an export format.  The native Philips format, iSyntax,
is a custom multi-file format not currently supported by OpenSlide.

The `ImageDescription` tag of the first TIFF directory contains an XML
document with a hierarchical structure containing key-value pairs.
The keys are based on DICOM tags.

The level dimensions given in the TIFF `ImageWidth` and `ImageLength`
fields, and also in the `ImageDescription` XML, are merely the TIFF tile
size multiplied by the number of tiles in each dimension.  Thus, they
include the size of the padding in the right-most column and bottom-most row
of tiles.  Each level typically uses the same tile size but requires a
different amount of padding, so the aspect ratios of the levels are
inconsistent and the level dimensions are not proportional to the level
downsamples.  Correct downsamples can be calculated from the levels'
pixel spacings in the XML metadata.

Slides with multiple regions of interest are structured as a single image
pyramid enclosing all regions.  Slides may omit pixel data for TIFF tiles
not in an ROI; this is represented as a `TileOffset` of 0 and a
`TileByteCount` of 0.  When such tiles are downsampled into a tile that
does contain pixel data, their contents are rendered as white pixels.

Label and macro images are stored as Base64-encoded JPEGs in the
`ImageDescription` XML.  Some slides also store these images as stripped
TIFF directories whose `ImageDescription`s start with `Label` and `Macro`,
respectively.


Relevant TIFF tags
------------------

Tag                 | Description                    |
--------------------|--------------------------------|
`ImageDescription`  |Stores an XML document containing various metadata and associated image data|
`Software`          |Starts with `Philips`           |


Associated Images
-----------------

`label`
: the TIFF directory with an `ImageDescription` starting with `Label`, or
the image data in the `DPScannedImage` with a `PIM_DP_IMAGE_TYPE` of
`LABELIMAGE`

`macro`
: the TIFF directory with an `ImageDescription` starting with `Macro`, or
the image data in the `DPScannedImage` with a `PIM_DP_IMAGE_TYPE` of
`MACROIMAGE`


Known Properties
----------------

All key-value data encoded in the `DPUfsImport` object, in the first
`DPScannedImage` object with a `PIM_DP_IMAGE_TYPE` of `WSI`, and in that
object's `PixelDataRepresentation` objects is represented as properties
prefixed with "`philips.`".

`openslide.mpp-x`
: calculated as `1000 * philips.DICOM_PIXEL_SPACING[1]`

`openslide.mpp-y`
: calculated as `1000 * philips.DICOM_PIXEL_SPACING[0]`


Test Data
---------

Some data is available in
[#137](https://github.com/openslide/openslide/issues/137) and
[#145](https://github.com/openslide/openslide/issues/145).  No
redistributable data is available.  Contact the
[mailing list][users-subscribe] if you can contribute some.
