---
layout: default
title: Leica format
---

Format
:single-file pyramidal tiled BigTIFF with non-standard metadata

File extensions
:`.scn`

OpenSlide vendor backend
:`leica`

OpenSlide ops backend
:`tiff`

Detection
---------

Leica slides are stored in single-file BigTIFF format.
OpenSlide will detect a file as Leica if:

 1. The file is TIFF.
 2. The `ImageDescription` tag contains valid XML in the namespace `http://www.leica-microsystems.com/scn/2010/10/01`.

To open Leica files, OpenSlide must be built with libtiff 4 or above.


Relevant TIFF tags
------------------

Tag                 | Description                    |
--------------------|--------------------------------|
`ImageDescription`|Stores an XML document containing various metadata|


TIFF Image Directory Organization
---------------------------------

Leica slides contain a pyramidal main image and a pyramidal macro image.
The XML document in the `ImageDescription` tag enumerates the TIFF
directories corresponding to each image.


Associated Images
-----------------

`macro`
:the highest-resolution `dimension` of the `image` whose `view` has the
same size as the containing `collection`


Known Properties
----------------

`leica.aperture`
:the `numericalAperture` of the main image

`leica.barcode`
:the `barcode` text

`leica.creation-date`
:the `creationDate` of the main image

`leica.device-model`
:the `device` `model` of the main image

`leica.device-version`
:the `device` `version` of the main image

`leica.illumination-source`
:the `illuminationSource` of the main image

`leica.objective`
:the `objective` of the main image

`openslide.mpp-x`
:calculated as `10000/tiff.XResolution`

`openslide.mpp-y`
:calculated as `10000/tiff.YResolution`

`openslide.objective-power`
:normalized `leica.objective`


Test Data
---------

<http://openslide.cs.cmu.edu/download/openslide-testdata/Leica/>
