---
layout: default
title: Ventana format
---

Format
: single-file pyramidal tiled BigTIFF with non-standard metadata and overlaps

File extensions
: `.bif`, `.tif`

OpenSlide vendor backend
: `ventana`


Detection
---------

Ventana slides are stored in single-file BigTIFF format.
OpenSlide will detect a file as Ventana if:

 1. The file is TIFF.
 2. The `XMP` tag contains valid XML.
 3. The XML contains an `iScan` element, either as the root element or as a child of a `Metadata` root element.


Associated Images
-----------------

`macro`
: the TIFF directory whose `ImageDescription` is `Label Image` or `Label_Image`

`thumbnail`
: the TIFF directory whose `ImageDescription` is `Thumbnail`


Known Properties
----------------

All XML attributes in the `iScan` element are represented as properties
prefixed with "`ventana.`".

`openslide.mpp-x`
: normalized `ventana.ScanRes`

`openslide.mpp-y`
: normalized `ventana.ScanRes`

`openslide.objective-power`
: normalized `ventana.Magnification`


Test Data
---------

<http://openslide.cs.cmu.edu/download/openslide-testdata/Ventana/>
