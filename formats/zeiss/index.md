---
title: Zeiss format
permalink: /formats/zeiss/
---

Format
: single-file binary format

File extensions
: `.czi`

OpenSlide vendor backend
: `zeiss`


## Detection

OpenSlide will detect a file as Zeiss if:

 1. The file is not a TIFF.
 2. The file has at least 32 bytes and starts with `ZISRAWFILE`.


## CZI format

CZI slides consist of overlapping image tiles at arbitrary pixel positions.
Tiles in level 0 are typically large, e.g. 2056 x 2464 pixels.  A slide may
or may not include downsampled levels.  Slides may include multiple scenes
(scan regions), whose pyramids can have different numbers of downsampled
levels.  Scenes are reflected in the metadata but aren't very important for
rendering the slide, since tile positions are relative to the slide and not
the scene.

The storage unit for an image tile is the subblock.  A subblock contains
pixel data, a small piece of XML metadata (which is ignored by OpenSlide),
and a directory entry containing the subblock's dimensions, pixel format,
and compression type.  Directory entries are stored alongside individual
subblocks, and a second copy of each entry is stored in an array whose
location is recorded in the file header.

A dimension represents coordinates along an axis; it contains a short string
identifying the dimension, an offset, and for some dimensions, a size in
level 0 and in the subblock's level.  Possible dimensions are "`X`" and
"`Y`" pixel coordinates, a scene identifier "`S`", a channel identifier
"`C`" (with value 0 for brightfield), and the tile's Z-index "`M`".  Higher
Z-indexes should be rendered after lower Z-indexes.  The downsample of a
subblock can be computed by dividing its `X` or `Y` size in level 0 by its
size in the subblock's level.

Pixel data may be compressed in any of several formats.  JPEG XR is common.
Uncompressed 24 bpp or 48 bpp pixel data is also possible, as well as pixel
data compressed with lossless [Zstandard][zstd] compression.  CZI's
Zstandard support comes in two flavors, zstd0 and zstd1, with the latter
prefixed by an uncompressed header typically three bytes long.  A flag in
that header indicates the presence of HiLo packing, in which the low bytes
of 16-bit color samples are packed together in the first half of the
uncompressed buffer and the high bytes in the second half.  CZI also permits
JPEG and LZW compression, though these do not appear to be common and
OpenSlide does not support them.

CZI files can embed arbitrary named attachments, which might be JPEG images,
nested CZI files, or other metadata.  The `Label` and `SlidePreview`
attachments are stored as nested CZIs and the `Thumbnail` attachment is
stored as a JPEG.

CZI also includes a large XML document containing scan parameters for the
slide.

[zstd]: https://facebook.github.io/zstd/


### Gamma values

Color images generated by at least Axioscan 7 scanners seem not to be gamma
corrected before storage, and appear dark.  The
`zeiss.Information.Instrument.Detectors.$camera_id.GammaDefault` property
(where `$camera_id` can be read from
`zeiss.Information.Image.Dimensions.Channels.Channel:0.DetectorSettings.Detector.Id`)
might be the recommended gamma correction for displaying CZI images.
Observed values include 0.45 for Axiocam705c and AxioCamEL color cameras and
1 for Axiocam712m monochrome cameras.


## Associated Images

`label`
: the `Label` attachment (optional)

`macro`
: the `SlidePreview` attachment (optional)

`thumbnail`
: the `Thumbnail` attachment (optional)


## Known Properties

Certain text nodes and attributes from the XML metadata are represented as
properties prefixed with "`zeiss.`".  The available properties are those
from the `AttachmentInfos`, `DisplaySetting`, `Information`, and `Scaling`
elements of `ImageDocument.Metadata`.

`openslide.mpp-x`
: calculated as 1000000 times `zeiss.Scaling.Items.X.Value`

`openslide.mpp-y`
: calculated as 1000000 times `zeiss.Scaling.Items.Y.Value`

`openslide.objective-power`
: normalized `zeiss.Information.Instrument.Objectives.$objective.NominalMagnification`
where the value of `$objective` is obtained from
`zeiss.Information.Image.ObjectiveSettings.ObjectiveRef.Id`


## Test Data

<https://openslide.cs.cmu.edu/download/openslide-testdata/Zeiss/>


## ImHex Patterns

- [CZI file](https://github.com/openslide/openslide/blob/main/misc/imhex/zeiss-czi.hexpat)