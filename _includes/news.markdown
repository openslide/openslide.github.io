OpenSlide version 3.4.0, 2014-01-25
-----------------------------------
OpenSlide 3.4.0 adds support for Hamamatsu NDPI, Leica slides with multiple
coplanar main images, MIRAX slides with PNG and BMP encodings, Sakura
SVSLIDE, and Ventana BIF (preliminary).  It also changes the Leica level
size/origin to encompass the entire slide, and improves compatibility with
certain MIRAX slides.

**API changes**: added new properties giving the bounds of the non-empty
slide region, added `openslide_detect_vendor()`, deprecated
`openslide_can_open()`.

OpenSlide Java version 0.12.0, 2014-01-25
-----------------------------------------
OpenSlide Java 0.12.0 updates the API for OpenSlide 3.4.0 and fixes a
`NullPointerException` when opening slides without a quickhash1.

OpenSlide Python version 0.5.0, 2014-01-25
------------------------------------------
OpenSlide Python 0.5.0 updates the API for OpenSlide 3.4.0, adds Python 3
support, returns Unicode strings on Python 2, adds a `DeepZoomGenerator`
option to render only the non-empty slide region, corrects Deep Zoom tile
positions for Aperio slides, fixes initialization on MacPorts, and improves
the Deep Zoom example tools.

New Windows build, 2013-07-27
-----------------------------
Windows build 20130727 prevents libtiff from opening a dialog box upon
encountering an invalid TIFF file.

OpenSlide version 3.3.3, 2013-04-13
-----------------------------------
Version 3.3.3 fixes inclusion of `openslide.h` with MSVC and adds minor
compatibility improvements for Aperio JP2K and Hamamatsu slides.

Windows build 20130413 also fixes a runtime crash when linked with
`/OPT:REF`.

OpenSlide version 3.3.2, 2012-12-01
-----------------------------------
Version 3.3.2 fixes seams in MIRAX 2.2 slides, fixes associated images in
single-level Aperio slides, and improves performance on MIRAX and Hamamatsu
VMU.

Windows build 20121201 also fixes a serious, Windows-specific thread safety
issue.


{% if page.news_show_extended %}

OpenSlide version 3.3.1, 2012-10-14
-----------------------------------
Version 3.3.1 has been released, parallelizing concurrent
`openslide_read_region` calls, improving performance on MIRAX and Hamamatsu
VMS, and adding experimental tile size properties.

OpenSlide now in MacPorts, 2012-09-23
-------------------------------------
Mac OS X users can now install OpenSlide from [MacPorts][macports].

[macports]: http://www.macports.org/

OpenSlide version 3.3.0, 2012-09-08
-----------------------------------
Version 3.3.0 adds support for Leica SCN files and preliminary support
for MIRAX 2.2, adds standard properties for microns-per-pixel and objective
power, and improves the command-line tools.

**API changes**: some functions were renamed and the old names deprecated,
`openslide_get_version` was added, and `openslide_open` now reports errors
by returning a handle in error state.

OpenSlide Java version 0.11.0, 2012-09-08
-----------------------------------------
Version 0.11.0 of the Java bindings renames some methods, adds APIs for
obtaining the versions of OpenSlide and the Java bindings, fixes error
handling under OpenSlide 3.3.0, and fixes many build problems.

OpenSlide Python version 0.4.0, 2012-09-08
------------------------------------------
Version 0.3.0 of the Python bindings renames some methods and properties,
adds a property for the OpenSlide library version, fixes error handling
under OpenSlide 3.3.0, and fixes initialization on Mac OS X.

OpenSlide user meeting in Baltimore
-----------------------------------
There will be an [informal gathering][baltimore] of OpenSlide users on
October 29, 2012 in Baltimore, MD.  Come by and introduce yourself!

[baltimore]: http://lists.andrew.cmu.edu/pipermail/openslide-users/2012-July/000387.html

Windows binaries now available, 2012-08-10
------------------------------------------
Compiled binaries for 32-bit and 64-bit Windows are now available from the
[download][download_win] page.

[download_win]: /download/#windows_binaries

VIPS now supports OpenSlide, 2012-04-17
---------------------------------------
The [VIPS image processing system][vips] can now read whole-slide images
with OpenSlide.

[vips]: http://www.vips.ecs.soton.ac.uk

OpenSlide version 3.2.6, 2012-02-23
-----------------------------------
Version 3.2.6 adds support for downsampled MIRAX files, improves
performance on some MIRAX slides, fixes a minor MIRAX drawing bug, and
fixes a 3.2.5 regression in openslide_read_region with large
dimensions.

OpenSlide Python version 0.3.0, 2011-12-16
------------------------------------------
Version 0.3.0 of the Python bindings fixes some crashes, adds Windows
support, adds methods for obtaining Deep Zoom tile coordinates, and
improves the example Deep Zoom tilers.

OpenSlide Java version 0.10.0, 2011-12-16
-----------------------------------------
Version 0.10.0 of the Java bindings renames the package and library files,
compiles using GNU Autotools, changes handling of associated images, and
fixes OpenSlideView translation by large offsets.

OpenSlide version 3.2.5, 2011-12-16
-----------------------------------
Version 3.2.5 has been released, supporting MIRAX 1.03 files, fixing
openslide_read_region for large dimensions, reducing memory usage,
disabling quickhash-1 for unusual TIFFs where it is very slow, and
fixing compilation errors.

OpenSlide Python version 0.2.0, 2011-09-02
------------------------------------------
The first release of the Python bindings includes complete access to the
OpenSlide API, functionality for producing Deep Zoom images, and a simple
web application for displaying whole-slide images in a browser.

OpenSlide version 3.2.4, 2011-03-07
-----------------------------------
Version 3.2.4 has been released, supporting MIRAX files without non-hierarchical sections,
working around some GKeyFile bugs, and fixing compilation errors on Windows.

OpenSlide version 3.2.3, 2010-09-09
-----------------------------------
Version 3.2.3 has been released, supporting more MIRAX files, adding a background color
property, fixing some MIRAX drawing bugs, and adding support for quickhash-1 on all
platforms.

OpenSlide Java version 0.9.2, 2010-08-10
----------------------------------------
Version 0.9.2 of the Java bindings removes some experimental CMU-specific annotation support.

OpenSlide Java version 0.9.1, 2010-06-16
----------------------------------------
Version 0.9.1 of the Java bindings fixes a Windows build bug and removes checks for negative coordinates and zero dimensions.

OpenSlide version 3.2.2, 2010-06-16
-----------------------------------
Version 3.2.2 has been released, adding support for negative coordinates and zero-sized dimensions in openslide_read_region, fixing a Windows build bug with new NGR support, and adding untested BigTIFF support.

OpenSlide version 3.2.1, 2010-06-03
-----------------------------------
Version 3.2.1 has been released, fixing Windows crashes, quieting down the error logging, and fixing problems with libjpeg 7.

OpenSlide Java version 0.9.0, 2010-06-01
----------------------------------------
Version 0.9.0 of the Java bindings adds support for the error handling system, eliminates the swig dependency, and adds new methods for painting.

OpenSlide version 3.2.0, 2010-06-01
-----------------------------------
Version 3.2.0 has been released, adding experimental CMake support and fixes for building with MSVC, an error handling mechanism, initial Hamamatsu Nanozoomer VMU support, and the "openslide-write-png" tool.

OpenSlide version 3.1.1, 2010-04-27
-----------------------------------
Version 3.1.1 has been released, fixing some bugs reading invalid VMS files. VMS files with multiple layers (NoLayers > 1) are also supported now, but the additional layers are ignored.

OpenSlide version 3.1.0, 2010-04-01
-----------------------------------
Version 3.1.0 has been released, which fixes problems with some TIFF files and adds support for certain newer Aperio files (compression 33005).

OpenSlide version 3.0.3, 2010-03-01
-----------------------------------
Version 3.0.3 has been released, which fixes nasty artifacts in some MIRAX files seen at some zoom levels.

OpenSlide version 3.0.2, 2010-02-17
-----------------------------------
Version 3.0.2 has been released, which restores the ability to build with glib 2.12, at the expense of not having "quickhash-1" in that configuration.

OpenSlide version 3.0.1, 2010-02-04
-----------------------------------
Version 3.0.1 has been released, with a fix for drawing the edges of TIFF files.

OpenSlide Java version 0.8.0, 2010-01-28
----------------------------------------
Version 0.8.0 of the Java bindings changes the license to LGPLv2, fixes some bugs, adds a new selection type, and adds a call to paint a specific layer without scaling.

OpenSlide version 3.0.0, 2010-01-28
-----------------------------------
Version 3.0.0 has been released, with a license change to LGPLv2, introduction of "quickhash-1", MIRAX bug fixes, and documentation improvements.

{% endif %}
