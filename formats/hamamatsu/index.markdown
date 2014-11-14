---
title: Hamamatsu format
permalink: /formats/hamamatsu/
redirect_from:
  - /Hamamatsu format/
---

Format
: multi-file JPEG/NGR with proprietary metadata and index file formats, and
single-file TIFF-like format with proprietary metadata

File extensions
: `.vms`, `.vmu`, `.ndpi`

OpenSlide vendor backend
: `hamamatsu`


Detection
---------

OpenSlide will detect a file as Hamamatsu if:

 1. The file given is a INI-style text file.
 2. It has a `[Virtual Microscope Specimen]` (VMS) or `[Uncompressed Virtual Microscope Specimen]` (VMU) group.
 3. If VMS, there are at least 1 row and 1 column of JPEG images (`NoJpegColumns` and `NoJpegRows`).

or if:

 1. The file has a TIFF directory structure.
 2. TIFF tag 65420 is present.


Overview
--------

The Hamamatsu format has three variants.  VMS and VMU consist of an index
file, 2 or more image files, and (in the case of VMS) an "optimisation"
file.  NDPI consists of a single TIFF-like file with some custom TIFF tags.
VMS and NDPI contain JPEG images; VMU contains NGR images (a custom
uncompressed format).

Multiple focal planes are ignored, only focal plane 0 is read.

JPEG does not allow for files larger than 65535 pixels on a side.  In VMS,
multiple JPEG files are used to encode large images.  To avoid having many
files, VMS uses close to maximum size (65K by 65K) JPEG files.  NDPI,
instead, stuffs large levels into a single JPEG and sets the overflowed
width/height fields to 0.

Unfortunately, JPEG provides very poor support for
random-access decoding of parts of a file. To get around this, JPEG
restart markers are placed at regular intervals, and these offsets are
specified in the optimisation file (in VMS) or in a TIFF tag (in NDPI).
With restart markers identified,
OpenSlide can treat JPEG as a tiled format, where the height is the
height of an MCU row, and the width is the number of MCUs per row
divided by the restart marker interval times the width of an
MCU. (This often leads to oddly-shaped and inefficient tiles of
4096x8, for example.)

Unfortunately, the VMS optimisation file does not give the location of
every restart marker, only the ones found at the beginning of an MCU
row. It also seems that the file ends early, and does not give the
location of the restart marker at the last MCU row of the last image
file.

Thus, the optimisation file can only be taken as a hint, and cannot be
trusted. The entire set of JPEG files must be scanned for restart
markers in order to facilitate random access. OpenSlide does this
lazily as needed, and also in a background thread that runs only when
OpenSlide is otherwise idle.

The VMS map file is a lower-resolution version of the other images, and
can be used to make a 2-level JPEG pyramid. JPEG also allows for
lower-resolution decoding, so further pyramid levels are synthesized
from each JPEG file.


VMS File
--------

The `.vms` file is the main index file for the VMS format. It is a
Windows INI-style key-value pair file, with sections. Only keys in the
`Virtual Microscope Specimen` group are read by OpenSlide.

Here are known keys from the file:

Key                    | Description                     |
-----------------------|---------------------------------|
`NoLayers`|Number of layers, currently must be 1 to be accepted|
`NoJpegColumns`|Number of JPEG files across, given in `ImageFile` attributes|
`NoJpegRows`|Number of JPEG files down, given in `ImageFile` attributes|
`ImageFile`|Semantically equivalent to `ImageFile(0,0,0)`, though not specified that way. The image in position (0,0,0) of the set of images|
`ImageFile(x,y)`|Semantically equivalent to `ImageFile(0,x,y)`, though not specified that way. The image in position (0,x,y) of the set of images|
`ImageFile(z,x,y)`|Where `x` and `y` are non-negative integers. Both `x` and `y` cannot be 0. `z` is a positive integer. These are the images that make up the virtual slide, as a concatenation of JPEG images. `x` and `y` specify the location of each JPEG, `z` specifies the focal plane|
`MapFile`|A lower-resolution version of all the ImageFiles|
`OptimisationFile`|File specifying some of the restart marker offsets in each ImageFile|
`AuthCode`|Unknown|
`SourceLens`|Apparently the objective power|
`PhysicalWidth`|Width of the main image in nm|
`PhysicalHeight`|Height of the main image in nm|
`LayerSpacing`|Unknown|
`MacroImage`|Image file for the "macro" associated image|
`PhysicalMacroWidth`|Width of the macro image in nm|
`PhysicalMacroHeight`|Height of the macro image in nm, sometimes with a trailing semicolon|
`XOffsetFromSlideCentre`|Distance in X from the center of the entire slide (i.e., the macro image) to the center of the main image, in nm|
`YOffsetFromSlideCentre`|Distance in Y from the center of the entire slide to the center of the main image, in nm|


VMU File
--------

The `.vmu` file is the main index file for the VMU format. Only keys in the `Uncompressed Virtual Microscope Specimen` group are read by OpenSlide.

Here are known keys from the file:

Key                 | Description                |
--------------------|----------------------------|
`NoLayers`|(see VMS above)|
`ImageFile`|(see VMS above)|
`ImageFile(x,y)`|(see VMS above)|
`ImageFile(z,x,y)`|(see VMS above)|
`MapFile`|(see VMS above)|
`MapScale`|Seems to be the downsample factor of the map|
`AuthCode`|(see VMS above)|
`SourceLens`|(see VMS above)|
`PixelWidth`|Width of the image in pixels|
`PixelHeight`|Height of the image in pixels|
`PhysicalWidth`|(see VMS above)|
`PhysicalHeight`|(see VMS above)|
`LayerSpacing`|(see VMS above)|
`LayerOffset`|Unknown|
`MacroImage`|(see VMS above)|
`PhysicalMacroWidth`|(see VMS above)|
`PhysicalMacroHeight`|(see VMS above)|
`XOffsetFromSlideCentre`|(see VMS above)|
`YOffsetFromSlideCentre`|(see VMS above)|
`Reference`|Unknown|
`BitsPerPixel`|Bits per pixel, currently expected to be 36|
`PixelOrder`|Currently expected to be RGB|
`Creator`|String describing the software creating this image|
`IlluminationMode`|Unknown|
`ExposureMultiplier`|Unknown, possibly the multiplier used to scale to 15 bits?|
`GainRed`|Unknown|
`GainGreen`|Unknown|
`GainBlue`|Unknown|
`FocalPlaneTolerance`|Unknown|
`NMP`|Unknown|
`MacroIllumination`|Unknown|
`FocusOffset`|Unknown|
`RefocusInterval`|Unknown|
`CubeName`|Unknown|
`HardwareModel`|Name of the hardware|
`HardwareSerial`|Serial number of the hardware|
`NoFocusPoints`|Unknown|
`FocusPoint0X`|Unknown|
`FocusPoint0Y`|Unknown|
`FocusPoint0Z`|Unknown|
`FocusPoint1X`|Unknown|
`FocusPoint1Y`|Unknown|
`FocusPoint1Z`|Unknown|
`FocusPoint2X`|Unknown|
`FocusPoint2Y`|Unknown|
`FocusPoint2Z`|Unknown|
`FocusPoint3X`|Unknown|
`FocusPoint3Y`|Unknown|
`FocusPoint3Z`|Unknown|
`NoBlobPoints`|Unknown|
`BlobPoint0Blob`|Unknown|
`BlobPoint0FocusPoint`|Unknown|
`BlobPoint1Blob`|Unknown|
`BlobPoint1FocusPoint`|Unknown|
`BlobPoint2Blob`|Unknown|
`BlobPoint2FocusPoint`|Unknown|
`BlobPoint3Blob`|Unknown|
`BlobPoint3FocusPoint`|Unknown|
`BlobMapWidth`|Unknown|
`BlobMapHeight`|Unknown|


NDPI File
---------

NDPI uses a TIFF-like structure, but libtiff cannot read the headers of an
NDPI file.  This is because NDPI specifies the `RowsPerStrip` as the height
of the file, and after doing out the multiplication, this typically
overflows libtiff and it refuses to open the file.  Also, the TIFF tags are
not stored in sorted order.

NDPI stores an image pyramid in TIFF directory entries.  In some files, the
lower-resolution pyramid levels contain no restart markers.  The macro
image, and sometimes an active-region map, seems to come last.

JPEG files in NDPI are not necessarily valid. If
`ImageWidth` or `ImageHeight` exceeds the JPEG limit of 65535, then
the width or height as stored in the JPEG file is 0. libjpeg will refuse
to read the header of such a file, so the JPEG data stream must be
altered when fed into libjpeg.

Here are the observed TIFF tags:

Tag          | Description      |
-------------|------------------|
`ImageWidth`|Width of the image|
`ImageHeight`|Height of the image|
`Make`|"Hamamatsu"|
`Model`|"NanoZoomer" or "C9600-12", etc|
`XResolution`|Seemingly correct X resolution, when interpreted with `ResolutionUnit`|
`YResolution`|Seemingly correct Y resolution, when interpreted with `ResolutionUnit`|
`ResolutionUnit`|Seemingly correct resolution unit|
`Software`|"NDP.scan", sometimes with a version number|
`StripOffsets`|The offset of the JPEG file for this layer|
`StripByteCounts`|The length of the JPEG file for this layer|
65420|Always exists, always 1.  File format version?|
65421|`SourceLens`, correctly downsampled for each entry. -1 for macro image, -2 for a map of non-empty regions.|
65422|`XOffsetFromSlideCentre`|
65423|`YOffsetFromSlideCentre`|
65424|Seemingly the Z offset from the center focal plane (in nm?)|
65425|Unknown, always 0?|
65426|Optimisation entries, as above|
65427|`Reference`|
65428|Unknown, `AuthCode`?|
65430|Unknown, have seen 0.0|
65433|Unknown, I have seen 1500 in this tag|
65439|Unknown, perhaps some polygon ROI?|
65440|Unknown, I have seen this: `<0 0 0 1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 1 9 1 10 1 11 1 12 1 13 1 14 1 15 1 16 1 17>`|
65441|Unknown, always 0?|
65442|Scanner serial number|
65443|Unknown, have seen 0 or 16|
65444|Unknown, always 80?|
65445|Unknown, have seen 0, 2, 10|
65446|Unknown, always 0?|
65449|ASCII metadata block, `key=value` pairs, not always present|
65455|Unknown, have seen 13|
65456|Unknown, have seen 101|
65457|Unknown, always 0?|
65458|Unknown, always 0?|


Optimisation File (only for VMS)
--------------------------------

The optimisation file contains a list of 32- (or 64- or 320- ?) bit
little endian values, giving the file offset into an MCU row, each
offset starts at a 40-byte alignment, and the last row (of the entire
file, not each image) seems to be missing. The offsets are all packed
into 1 file, even with multiple images. The order of images is
left-to-right, top-to-bottom.


Map File (only for VMS/VMU)
---------------------------

The VMS map file is a standard JPEG file. Its restart markers (if any)
are not included in the optimisation file. The VMU map file is in NGR
format. This file can be used to provide a lower-resolution view of
the slide.


Image Files (only for VMS/VMU)
------------------------------

These files are given by the VMS/VMU `ImageFile` keys. They are
assumed to have a height which is a multiple of the MCU height. They
are assumed to have a width which is a multiple of MCUs per row
divided by the restart interval.

For VMS, these files are in JPEG, for VMU they are in NGR format.


NGR Format
----------

The NGR file contains uncompressed 16-bit RGB data, with a small
header. The files we have encountered start with `GN`, two more bytes,
and then width, height, and column width in little endian 32-bit
format. The column width must divide evenly into the width. Column
width is important, since NGR files are generated in columns, where
the first column comes first in the file, followed by subsequent
files. Columns are painted left-to-right.

At offset 24 is another 32-bit integer which gives the offset in the file to the start of the image data. The image data we have encountered is in 16-bit little endian format.


Associated Images
-----------------

macro
: the image file given by the `MacroImage` value in the VMS/VMU file, or
`SourceLens` of -1 in NDPI


Known Properties
----------------

All key-value data stored in the VMS/VMU file, and known tags from
the NDPI file, are encoded as properties prefixed with "`hamamatsu.`".

`openslide.mpp-x`
: for NDPI, calculated as `10000/tiff.XResolution`, if `tiff.ResolutionUnit`
is `centimeter`

`openslide.mpp-y`
: for NDPI, calculated as `10000/tiff.YResolution`, if `tiff.ResolutionUnit`
is `centimeter`

`openslide.objective-power`
: normalized `hamamatsu.SourceLens`


Test Data
---------
NDPI format
: <http://openslide.cs.cmu.edu/download/openslide-testdata/Hamamatsu/>

VMS format
: <http://openslide.cs.cmu.edu/download/openslide-testdata/Hamamatsu-vms/>
