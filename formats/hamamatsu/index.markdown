---
layout: default
title: Hamamatsu format
---

Format
:multi-file JPEG/NGR with proprietary metadata and index file formats

File extensions
:`.vms`, `.vmu`

OpenSlide vendor backend
:`hamamatsu`

OpenSlide ops backend
:`jpeg` for `.vms`, `ngr` for `.vmu`


Detection
---------

OpenSlide will detect a file as Hamamatsu if:

 1. The file given is a INI-style text file.
 2. It has a `[Virtual Microscope Specimen]` (VMS) or `[Uncompressed Virtual Microscope Specimen]` (VMU) group.
 3. The file specifies a positive number of layer (`NoLayers>=1`). Currently, only one of these focal plane layers is read.
 4. If VMS, there are at least 1 row and 1 column of JPEG images (`NoJpegColumns` and `NoJpegRows`).
 5. The mapfile given by `MapFile` is a valid readable file in the same directory as the VMS file.
 6. The files given by the various `ImageFile` lines do not exceed the number of rows and columns as specified above.
 7. The mapfile and image files are all valid JPEG files or all valid NGR files.
 8. The restart interval in each JPEG file is zero, or evenly divides into the number of MCUs per row.
 9. The image files (except the map file) all have the same "tile" sizes (see below).


Overview
--------

The Hamamatsu format consists of an index file (VMS or VMU), 2 or more
image files, and (in the case of VMS) an "optimisation" file.

Multiple focal planes are ignored, only focal plane 0 is read.

Because JPEG does not allow for large files, multiple JPEG files are
needed to encode large images. To avoid having many files, the
Hamamatsu format uses close to maximum size (65K by 65K) JPEG files.

Unfortunately, (unlike TIFF) JPEG provides very poor support for
random-access decoding of parts of a file. To get around this, JPEG
restart markers are placed at regular intervals, and these offsets are
specified in the optimisation file. With restart markers identified,
OpenSlide can treat JPEG as a tiled format, where the height is the
height of an MCU row, and the width is the number of MCUs per row
divided by the restart marker interval times the width of an
MCU. (This often leads to oddly-shaped and inefficient tiles of
8x2048, for example.)

Unfortunately, the optimisation file does not give the location of
every restart marker, only the ones found at the beginning of an MCU
row. It also seems that the file ends early, and does not give the
location of the restart marker at the last MCU row of the last image
file.

Thus, the optimisation file can only be taken as a hint, and cannot be
trusted. The entire set of JPEG files must be scanned for restart
markers in order to facilitate random access. OpenSlide does this
lazily as needed, and also in a background thread that runs only when
OpenSlide is otherwise idle.

The map file is a lower-resolution version of the other images, and
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
`SourceLens`|Apparently the magnification|
`PhysicalWidth`|Width of the slide in some unit?|
`PhysicalHeight`|Height of the slide in some unit?|
`LayerSpacing`|Unknown|
`MacroImage`|Image file for the "macro" associated image|
`PhysicalMacroWidth`|Unknown|
`PhysicalMacroHeight`|Unknown|
`XOffsetFromSlideCentre`|Unknown|
`YOffsetFromSlideCentre`|Unknown|


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


Optimisation File (only for VMS)
--------------------------------

The optimisation file contains a list of 32- (or 64- or 320- ?) bit
little endian values, giving the file offset into an MCU row, each
offset starts at a 40-byte alignment, and the last row (of the entire
file, not each image) seems to be missing. The offsets are all packed
into 1 file, even with multiple images. The order of images is
left-to-right, top-to-bottom.


Map File
--------

The VMS map file is a standard JPEG file. Its restart markers (if any)
are not included in the optimisation file. The VMU map file is in NGR
format. This file can be used to provide a lower-resolution view of
the slide.


Image Files
-----------

These files are given by the various `ImageFile` keys. They are
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
:the image file given by the `MacroImage` value in the VMS/VMU file


Known Properties
----------------

All key-value data stored in the VMS/VMU file are encoded as properties prefixed with "`hamamatsu.`".

`openslide.objective-power`
:normalized `hamamatsu.SourceLens`


Test Data
---------
<http://openslide.cs.cmu.edu/download/openslide-testdata/Hamamatsu/>
(ndpi format, wrapped vms format, currently not readable by OpenSlide)

<http://openslide.cs.cmu.edu/download/openslide-testdata/Hamamatsu-vms/> (vms format)

Preliminary NDPI Notes
----------------------

NDPI is basically VMS stuffed into a broken TIFF file. libtiff cannot
read the headers of a TIFF file, because NDPI specifies the
`RowsPerStrip` as the height of the file, and after doing out the
multiplication, this typically overflows libtiff and it refuses to
open the file. Also, the TIFF tags are not stored in sorted order
(sometimes, they may have fixed this in later versions).

Unlike the VMS format, the NDPI is stored in a pyramid format as TIFF
directory entries. The macro image seems to come last.

If one just reads the TIFF tags directly, perhaps using `tiffdump`, one will find:

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
65420|Unknown, always 1?|
65421|Magnification? `SourceLens` from VMS? Seems correctly downsampled for each entry. (-1 for macro image, -2 for some sort of mask?)|
65422|`XOffsetFromSlideCentre`|
65423|`YOffsetFromSlideCentre`|
65424|Unknown, always 0?|
65425|Unknown, always 0?|
65426|Optimisation entries, as above|
65427|Unknown, possibly slide identifier|
65428|Unknown, `AuthCode`?|
65433|Unknown, I have seen 1500 in this tag|
65439|Unknown, perhaps some polygon ROI?|
65440|Unknown, I have seen this: `<0 0 0 1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 1 9 1 10 1 11 1 12 1 13 1 14 1 15 1 16 1 17>`|
65441|Unknown, always 0?|
65442|Seems to be `Model`|
65443|Unknown, always 0?|
65444|Unknown, always 80?|
65445|Unknown, have seen 0 or 2|
65446|Unknown, always 0?|
65449|ASCII metadata block, not always present|


Unlike in VMS, JPEG files in NDPI are not necessarily valid. If
`ImageWidth` or `ImageHeight` exceeds the JPEG limit of 65535, then
the width or height as stored in the JPEG file is 0. JPEG files are
not split into validly-sized files like in VMS. libjpeg will refuse to
read the header of such a file, so the JPEG data stream must be
altered when fed into libjpeg. Since a random access source manager is
already required to read VMS JPEG files, this change is not too bad.