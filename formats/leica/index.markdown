---
title: Leica format
---

Format
: single-file pyramidal tiled BigTIFF with non-standard metadata

File extensions
: `.scn`

OpenSlide vendor backend
: `leica`


Detection
---------

Leica slides are stored in single-file BigTIFF format.
OpenSlide will detect a file as Leica if:

 1. The file is TIFF.
 2. The initial image is tiled.
 3. The `ImageDescription` tag contains valid XML in the namespace `http://www.leica-microsystems.com/scn/2010/10/01`.

To open Leica files, OpenSlide must be built with libtiff 4 or above.


Relevant TIFF tags
------------------

Tag                 | Description                    |
--------------------|--------------------------------|
`ImageDescription`|Stores an XML document containing various metadata|


File Organization
-----------------

The `ImageDescription` tag of the first TIFF directory contains an XML
document that defines the structure of the slide.

Leica slides are structured as a collection of images, each of which has
multiple dimensions (pyramid levels).  The collection has a size, and images
have a size and position, in a high-resolution unit which OpenSlide calls
"clicks".  Each dimension has a size in pixels, an optional focal plane
number, and a TIFF directory containing the image data.  Fluorescence images
have different dimensions (and thus different TIFF directories) for each
channel.  OpenSlide currently rejects fluorescence images and ignores focal
planes other than plane 0.

Brightfield slides have at least two images: a low-resolution macro image
and one or more main images corresponding to regions of the macro image.
The macro image has a position of (0, 0) and a size matching the size of the
collection.  Fluorescence slides can have two macro images: one brightfield
and one fluorescence.

The slide provides enough information to composite the various images,
including the macro image, into a single pyramid.  However, there are some
complications:

- The resolution of the macro image is generally not related to the
resolution of the main images by a power of two.
- Downsampled dimensions are generally downsampled from the next larger
dimension by a factor of 4, but main images can be scanned with distinct
objectives that may differ by only a factor of 2.

Thus, in general, the images in a collection cannot be rendered into a
unified pyramid without scaling the original pixel data.  OpenSlide does not
attempt to do this.  Instead, OpenSlide omits the macro image from the
pyramid and refuses to open slides whose main images have inconsistent
resolutions.


Associated Images
-----------------

`macro`
: the highest-resolution dimension of the macro image


Known Properties
----------------

`leica.aperture`
: the `numericalAperture` of the main image

`leica.barcode`
: the `barcode` text

`leica.creation-date`
: the `creationDate` of the main image

`leica.device-model`
: the `device` `model` of the main image

`leica.device-version`
: the `device` `version` of the main image

`leica.illumination-source`
: the `illuminationSource` of the main image

`leica.objective`
: the `objective` of the main image

`openslide.mpp-x`
: calculated as `10000/tiff.XResolution`, if `tiff.ResolutionUnit` is
`centimeter`

`openslide.mpp-y`
: calculated as `10000/tiff.YResolution`, if `tiff.ResolutionUnit` is
`centimeter`

`openslide.objective-power`
: normalized `leica.objective`


Test Data
---------

<http://openslide.cs.cmu.edu/download/openslide-testdata/Leica/>
