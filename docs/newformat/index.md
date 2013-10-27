Adding a new slide format to OpenSlide
--------------------------------------

To add a new format to OpenSlide, you will need to write a new vendor driver.  When a slide is opened, the driver is responsible for parsing the slide file, loading its metadata, and locating its image tiles.  At runtime, the driver receives requests for pixel data, determines which tiles to load, decodes them to a buffer in a [Cairo-compatible pixel format](http://cairographics.org/manual/cairo-Image-Surfaces.html#cairo-format-t), and renders them to a [Cairo](http://cairographics.org/) surface.

Your driver can use the *grid* module to map pixel coordinates to tile addresses.  The `simple` grid is suitable for slide formats that have non-overlapping, regularly-spaced, equal-sized tiles, and do not need to record individual information about each tile.  (TIFF images often have this property.)  The `tilemap` grid is suitable for overlapping, irregular, or sparse tiles.

Your driver should use the *cache* module to cache pixel data from decoded tiles.  This prevents unnecessary decode operations if a region is accessed repeatedly.

OpenSlide contains support code for reading BMP, JPEG, JPEG 2000, PNG, TIFF, and TIFF-like images.  You may be able to use these utilities without modification.  If your driver requires additional decoding functionality, it should be added to a decoder module if it would be useful to other drivers, or implemented in your driver if not.

Drivers are named after the vendor of the product that uses the format.  This is often the manufacturer of the slide scanner.

For examples, consult the existing vendor drivers.  `generic-tiff` is a straightforward driver for simple TIFF images.  `trestle` is a fairly simple driver using the `tilemap` grid.

Opening a slide
---------------

Opening a slide occurs in two steps, implemented via function pointers in `struct _openslide_format`.

- The `detect` method should do some inexpensive tests to verify that the specified file is supported by your driver.  If `detect` fails, OpenSlide will continue trying other format drivers.  If the `OPENSLIDE_DEBUG` environment variable is set to `detection`, OpenSlide will use `g_message()` to log the error message returned by `detect`.

- The `open` method initializes the `openslide_t` with the information that will be needed at runtime.  `open` will never be called unless `detect` has succeeded.  If `open` fails, OpenSlide will consider this a hard failure, and `openslide_open()` will return a `openslide_t` in error state.  This can occur if the file appears to be a slide that should be supported by your driver, but is not structured in the expected way.  (Perhaps the slide uses a variant of the format that the driver does not yet support.)  

TIFF and TIFF-like
------------------

OpenSlide has two decoders for TIFF-derived slide formats: `tiff` and `tifflike`.

- `tiff` uses libtiff to read the slide file.  Most drivers for TIFF-based formats use this decoder.  libtiff can parse TIFF directories, decode image data in compression formats described in the TIFF specification, and return compressed image data for all other compression formats.  Because libtiff has a deep understanding of the TIFF tag values, it will reject files that use the TIFF directory structure but make creative use of the standard tags.

- `tifflike` is a TIFF directory parser built into OpenSlide.  It does not understand tag values and cannot decode compressed image data; it simply reads the TIFF directories and reports on what they contain.  This decoder can be used for formats that use the standard TIFF tags in unusual ways.

All `detect` and `open` methods receive a `tifflike` handle as an argument; this will be NULL if the file does not appear to be a TIFF.  Because `detect` should be inexpensive, it should do its work using that `tifflike` handle, and should not use the `tiff` decoder.  `open`, however, can use the `tiff` decoder if desired.  Note that OpenSlide will close the `tifflike` handle when the `open` method completes, so the driver should copy any information it needs out of the `tifflike` handle during `open`.

Properties
----------

The vendor driver is responsible for initializing a property map containing metadata about the slide.  A property has a name (a string) and a value (another string).  Property names defined by your driver should be prefixed by your driver’s name followed by a dot.  You should create properties for any and all metadata supported by your slide format.  If the slide format contains textual metadata formatted as key-value pairs, you may dump this metadata directly into the property map, retaining the original key names (after prepending the name of the driver).  If you need to invent your own key names, you should use `lowercase-with-hyphens` formatting.

Drivers for TIFF-derived formats should also call `_openslide_tifflike_init_properties_and_hash()` to set some standard properties pertaining to TIFF files.

Your driver is also responsible for setting some standard properties:

* `openslide.background-color`, if applicable
* `openslide.comment`, if applicable
* `openslide.mpp-x`, if possible.  Should be a double.
* `openslide.mpp-y`, if possible.  Should be a double.
* `openslide.objective-power`, if possible.  Should be an integer.
* `openslide.vendor`

`openslide.background-color` should be set with `_openslide_set_background_color_prop()`.

`openslide.mpp-x`, `openslide.mpp-y`, and `openslide.objective-power` should be a copy of, or otherwise derived from, another vendor-specific property.  The vendor-specific property should be the uninterpreted value from the slide file, while the `openslide.` property should be the validated or calculated value, often produced with `_openslide_duplicate_{int,double}_prop()`.

You should not set `openslide.quickhash-1` yourself; see below.

For examples of properties produced by existing drivers, see the [web demo](http://openslide.org/demo/).

### quickhash-1

When opening a slide, OpenSlide calculates a "quickhash-1" which uniquely identifies that particular slide.  (The quickhash-1 can be accessed via the `openslide.quickhash-1` property.)  It is implemented as a SHA-256 digest of a small amount of metadata and data from the slide file.  It is *not* intended as a cryptographic hash over the entire file.

If you call `_openslide_tifflike_init_properties_and_hash()`, that function will calculate the quickhash-1 for you.  Otherwise, you will need to handle this calculation yourself.  Your `open` function will receive an `_openslide_hash` handle; you should use the `_openslide_hash` helper functions to add the data you wish to include in the quickhash-1.

You should carefully select the data and metadata to be included in the quickhash.  Once your driver has been included in an OpenSlide release, it will be difficult or impossible to change the quickhash definition for your slide format.  The quickhash should not cover too much data, so that it is quick to calculate, but should never produce the same value for two different slides.  To accomplish this, it may be sufficient to hash all of the slide's metadata; if not, you can include the (compressed) image data from the lowest-resolution pyramid level.

Associated images
-----------------

In some slide formats, a slide file includes not only the primary, high-resolution slide image, but additional ancillary images.  For example, there might be a thumbnail of the entire slide, or a photograph of its paper label.  OpenSlide calls these "associated images" and provides an API to access them.

Where feasible, your driver should provide access to any associated images stored with the slide.  Each associated image has a short name; existing names are:

<dl>
<dt>label
<dd>the paper label (or barcode) glued to the slide
<dt>macro
<dd>a photograph of the entire slide, possibly extending beyond the edges of the glass
<dt>thumbnail
<dd>a low-resolution version of the primary image
</dl>

Use your judgement in assigning names to the associated images supported by your slide format.

OpenSlide currently does not support pyramidal associated images; each associated image is loaded into memory in its entirety.  If an associated image is pyramidal but is not too large, your driver can simply provide the highest-resolution level.

Error handling
--------------

OpenSlide takes a conservative approach to error handling.  Where feasible, a vendor driver should validate any slide metadata it is relying upon.  If the driver finds evidence that its understanding of the slide format is incomplete -- for example, required slide metadata is missing, or an enumerated field has an unknown value -- it should report an error and give up rather than attempting to muddle onward.

All internal OpenSlide functions report errors using GError.  GError has a [strict set of rules](http://developer.gnome.org/glib/stable/glib-Error-Reporting.html#glib-Error-Reporting.description) that **must** be followed when producing or consuming errors.

When the external API glue receives a GError from a handler method, the `openslide_t` is placed into error state.  No other operations can be performed on the `openslide_t`.  The GError `message` is made available to the application via the `openslide_get_error()` API call.

When producing a GError, you may use whatever error domain and code is appropriate.  If in doubt, use `OPENSLIDE_ERROR_FAILED`.

If you receive a GError from lower-level code and intend to propagate it, consider whether the error's `message` provides enough context to diagnose the failure.  If not, you should prefix the error using `g_prefix_error()` or `g_propagate_prefixed_error()`.

OpenSlide limitations
---------------------

OpenSlide's output is currently [limited to three color channels plus an alpha channel](https://github.com/openslide/openslide/issues/42), with a [maximum of 8 bits per channel](https://github.com/openslide/openslide/issues/41).  These restrictions are partially due to [Cairo](http://cairographics.org/) limitations, but correcting them would also require changes to the OpenSlide API.

In addition, OpenSlide currently [cannot return data from more than one focal plane per slide](https://github.com/openslide/openslide/issues/31).  This would also require API changes to fix.

Contributing your code
----------------------

Please discuss your changes on the [openslide-users](http://lists.andrew.cmu.edu/mailman/listinfo/openslide-users/) mailing list, *before* you are ready to submit them, so that we can help you integrate your code into the existing codebase.  You may also find the [[generic advice on contributing to OpenSlide|ContributingPatches]] helpful.

When contributing support for a new format, we *strongly* prefer that you also contribute example slide files for our [openslide-testdata](http://openslide.cs.cmu.edu/download/openslide-testdata/) repository.  The example files must be data that you are entitled to contribute, and the OpenSlide project must receive permission to redistribute them with or without modification.  Email the mailing list for instructions on how to accomplish this.