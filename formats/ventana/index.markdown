---
layout: default
title: Ventana format
---

Format
: single-file pyramidal tiled BigTIFF with non-standard metadata and overlaps

File extensions
: `.bif`

OpenSlide vendor backend
: `ventana`


Detection
---------

Ventana slides are stored in single-file BigTIFF format.
OpenSlide will detect a file as Ventana if:

 1. The file is TIFF.
 2. One of the TIFF levels has an `ImageDescription` containing the string `level=0`.
 3. That level has an XMP field containing valid XML, with a root tag of `EncodeInfo` and containing the string `iScan`.

To open Ventana files, OpenSlide must be built with libtiff 4 or above.


Associated Images
-----------------

`macro`
: the TIFF directory whose `ImageDescription` is `Label Image` or `Label_Image`

`thumbnail`
: the TIFF directory whose `ImageDescription` is `Thumbnail`


Known Properties
----------------

All XML attributes in the `/EncodeInfo/SlideInfo/iScan` element are
represented as properties prefixed with "`ventana.`".

`openslide.mpp-x`
: normalized `ventana.ScanRes`

`openslide.mpp-y`
: normalized `ventana.ScanRes`

`openslide.objective-power`
: normalized `ventana.Magnification`


Test Data
---------

<http://openslide.cs.cmu.edu/download/openslide-testdata/Ventana/>
