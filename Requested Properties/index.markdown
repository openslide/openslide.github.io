---
layout: default
title: Requested Properties
---

Future versions of OpenSlide will support new properties that start
with "`openslide.`". This page contains some requested properties and
from what vendor-specific properties we might derive them from.


proposed name|description|aperio|hamamatsu|trestle|mirax|leica|
-------------|-----------|------|---------|-------|-----|-----|
|`openslide.mpp-x`|Microns-per-pixel in the X dimension (requires an accurate objective property?)|`aperio.MPP`|maybe related to `hamamatsu.PhysicalWidth`?|`tiff.XResolution` (note that this is a totally non-standard use of this TIFF tag)|`mirax.LAYER_0_LEVEL_0_SECTION.MICROMETER_PER_PIXEL_X` (or whatever the correct layer and levels are)|`tiff.XResolution` (trivially derived from objective power)|
|`openslide.mpp-y`|Microns-per-pixel in the Y dimension (requires an accurate objective property?)|`aperio.MPP`|maybe related to `hamamatsu.PhysicalHeight`?|`tiff.YResolution` (see note for `tiff.XResolution`)|`mirax.LAYER_0_LEVEL_0_SECTION.MICROMETER_PER_PIXEL_Y` (or whatever the correct layer and levels are)|`tiff.YResolution` (trivially derived from objective power)|
|`openslide.objective-power`|Magnification power of the objective (this is often inaccurate)|`aperio.AppMag`?|`hamamatsu.SourceLens`?|`trestle.Objective Power`|`mirax.GENERAL.OBJECTIVE_MAGNIFICATION`|`leica.objective`|
