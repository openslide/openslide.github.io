{% include links.md %}

## Fedora and Enterprise Linux Copr now available, 2023-10-11

OpenSlide now provides a [Fedora Copr][download-copr], enabling Fedora
and RHEL-compatible Enterprise Linux users to easily install the latest
OpenSlide and OpenSlide Python releases before they reach Fedora or EPEL.


## OpenSlide version 4.0.0, 2023-10-11

OpenSlide 4.0.0 adds support for DICOM WSI slides, ICC color profiles, tile
cache customization, adds the `slidetool` command-line utility, removes
deprecated APIs, and improves format compatibility.

Windows build 20231011 integrates all dependencies into the OpenSlide DLL,
replaces the separate command-line tools with `slidetool`, and switches
from MSVCRT to the
[Universal C Runtime](https://learn.microsoft.com/en-us/cpp/windows/universal-crt-deployment)
(UCRT).


## Ubuntu PPA now available, 2023-10-11

OpenSlide now provides an [Ubuntu PPA][download-ppa], enabling Ubuntu
users to easily install the latest OpenSlide and OpenSlide Python releases
before they reach Ubuntu.


## OpenSlide Python version 1.3.1, 2023-10-08

OpenSlide Python 1.3.1 updates the docs and example tools to transform
images to sRGB using the default rendering intent of the image's ICC
profile, rather than absolute colorimetric intent.


## OpenSlide Python version 1.3.0, 2023-07-22

OpenSlide Python 1.3.0 adds support for the upcoming OpenSlide 4.0.0 and
drops support for Python 3.7.  It also exposes color management profiles
where available, and updates the Deep Zoom example tools to transform images
to sRGB by default.


## New Windows build, 2023-04-14

Windows build 20230414 integrates most dependencies into the OpenSlide
DLL, and also updates various dependencies.


## New Windows build, 2022-12-17

Windows build 20221217 updates OpenSlide Java and several dependencies.


## OpenSlide Java version 0.12.3, 2022-12-17

OpenSlide Java 0.12.3 adds a Meson build system, deprecates the
Autotools+Ant one, and fixes builds on newer JDKs.


{% if page.news_show_extended %}

## New Windows build, 2022-11-11

Windows build 20221111 updates the versions of many dependencies.


## New Windows build, 2022-08-11

Windows build 20220811 fixes crashes in the 64-bit binaries when reading
invalid JPEG or PNG images.


## New Windows build, 2022-08-06

Windows build 20220806 updates the compiler and all dependencies to current
versions.


## OpenSlide Python version 1.2.0, 2022-06-17

OpenSlide Python 1.2.0 drops support for Python older than 3.7.  It also
supports cache customization with OpenSlide 3.5.0, improves pixel read
performance, and improves installation documentation.


## OpenSlide Python version 1.1.2, 2020-09-13

OpenSlide Python 1.1.2 fixes compatibility with setuptools &ge; 46, Python
3.9, and Sphinx 2.x.


## New Windows build, 2017-11-22

Windows build 20171122 updates the versions of many dependencies.


## OpenSlide Java version 0.12.2, 2016-09-11

OpenSlide Java 0.12.2 fixes builds on JDK 9 and on Mac OS X.


## New Windows build, 2016-07-17

Windows build 20160717 updates OpenJPEG to version 2.1.1.


## New Windows build, 2016-06-12

Windows build 20160612 fixes crashes in the 32-bit binaries when called
from code compiled with MSVC.


## OpenSlide Python version 1.1.1, 2016-06-11

OpenSlide Python 1.1.1 changes the default Deep Zoom tile size to 254 pixels
to improve viewer performance.  It also fixes exceptions with Pillow 3.x and
with large reads when the extension module is not installed.


## New Windows build, 2015-05-27

Windows build 20150527 fixes crashes in the 32-bit binaries.


## OpenSlide version 3.4.1, 2015-04-20

OpenSlide 3.4.1 adds support for Philips TIFF and Ventana TIFF, improves the
performance of JPEG and JP2K decoding, and adds support for OpenJPEG 2.1.0.
It also includes fixes and improvements for Aperio, Hamamatsu, Leica,
Sakura, and Ventana slides, as well as many portability fixes.

Windows build 20150420 also adds separate debug symbols for all binaries.


## OpenSlide Python version 1.1.0, 2015-04-20

OpenSlide Python 1.1.0 adds an extension module which significantly improves
pixel read performance.  The example viewers now display a scale bar via the
OpenSeadragonScalebar plugin.


## OpenSlide Java version 0.12.1, 2015-04-20

OpenSlide Java 0.12.1 improves support for cross-building for Windows from
newer Linux distributions.


## OpenSlide Python version 1.0.1, 2014-03-09

OpenSlide Python 1.0.1 fixes documentation build failures.


## OpenSlide Python version 1.0.0, 2014-03-09

OpenSlide Python 1.0.0 declares a stable API and adds documentation.


## OpenSlide Python version 0.5.1, 2014-01-26

OpenSlide Python 0.5.1 fixes exceptions on Python 2.6 and with the classic
PIL library.


## OpenSlide version 3.4.0, 2014-01-25

OpenSlide 3.4.0 adds support for Hamamatsu NDPI, Leica slides with multiple
coplanar main images, MIRAX slides with PNG and BMP encodings, Sakura
SVSLIDE, and Ventana BIF (preliminary).  It also changes the Leica level
size/origin to encompass the entire slide, and improves compatibility with
certain MIRAX slides.

**API changes**: added new properties giving the bounds of the non-empty
slide region, added `openslide_detect_vendor()`, deprecated
`openslide_can_open()`.


## OpenSlide Java version 0.12.0, 2014-01-25

OpenSlide Java 0.12.0 updates the API for OpenSlide 3.4.0 and fixes a
`NullPointerException` when opening slides without a quickhash1.


## OpenSlide Python version 0.5.0, 2014-01-25

OpenSlide Python 0.5.0 updates the API for OpenSlide 3.4.0, adds Python 3
support, returns Unicode strings on Python 2, adds a `DeepZoomGenerator`
option to render only the non-empty slide region, corrects Deep Zoom tile
positions for Aperio slides, fixes initialization on MacPorts, and improves
the Deep Zoom example tools.


## New Windows build, 2013-07-27

Windows build 20130727 prevents libtiff from opening a dialog box upon
encountering an invalid TIFF file.


## OpenSlide version 3.3.3, 2013-04-13

Version 3.3.3 fixes inclusion of `openslide.h` with MSVC and adds minor
compatibility improvements for Aperio JP2K and Hamamatsu slides.

Windows build 20130413 also fixes a runtime crash when linked with
`/OPT:REF`.


## OpenSlide version 3.3.2, 2012-12-01

Version 3.3.2 fixes seams in MIRAX 2.2 slides, fixes associated images in
single-level Aperio slides, and improves performance on MIRAX and Hamamatsu
VMU.

Windows build 20121201 also fixes a serious, Windows-specific thread safety
issue.


## OpenSlide version 3.3.1, 2012-10-14

Version 3.3.1 has been released, parallelizing concurrent
`openslide_read_region` calls, improving performance on MIRAX and Hamamatsu
VMS, and adding experimental tile size properties.


## OpenSlide now in MacPorts, 2012-09-23

Mac OS X users can now install OpenSlide from [MacPorts][macports].

[macports]: https://www.macports.org/


## OpenSlide version 3.3.0, 2012-09-08

Version 3.3.0 adds support for Leica SCN files and preliminary support
for MIRAX 2.2, adds standard properties for microns-per-pixel and objective
power, and improves the command-line tools.

**API changes**: some functions were renamed and the old names deprecated,
`openslide_get_version` was added, and `openslide_open` now reports errors
by returning a handle in error state.


## OpenSlide Java version 0.11.0, 2012-09-08

Version 0.11.0 of the Java bindings renames some methods, adds APIs for
obtaining the versions of OpenSlide and the Java bindings, fixes error
handling under OpenSlide 3.3.0, and fixes many build problems.


## OpenSlide Python version 0.4.0, 2012-09-08

Version 0.3.0 of the Python bindings renames some methods and properties,
adds a property for the OpenSlide library version, fixes error handling
under OpenSlide 3.3.0, and fixes initialization on Mac OS X.


## OpenSlide user meeting in Baltimore

There will be an [informal gathering][baltimore] of OpenSlide users on
October 29, 2012 in Baltimore, MD.  Come by and introduce yourself!

[baltimore]: https://lists.andrew.cmu.edu/pipermail/openslide-users/2012-July/000387.html


## Windows binaries now available, 2012-08-10

Compiled binaries for 32-bit and 64-bit Windows are now available from the
[download][download-windows] page.


## VIPS now supports OpenSlide, 2012-04-17

The [VIPS image processing system][vips] can now read whole-slide images
with OpenSlide.

[vips]: https://www.libvips.org/


## OpenSlide version 3.2.6, 2012-02-23

Version 3.2.6 adds support for downsampled MIRAX files, improves
performance on some MIRAX slides, fixes a minor MIRAX drawing bug, and
fixes a 3.2.5 regression in openslide_read_region with large
dimensions.


## OpenSlide Python version 0.3.0, 2011-12-16

Version 0.3.0 of the Python bindings fixes some crashes, adds Windows
support, adds methods for obtaining Deep Zoom tile coordinates, and
improves the example Deep Zoom tilers.


## OpenSlide Java version 0.10.0, 2011-12-16

Version 0.10.0 of the Java bindings renames the package and library files,
compiles using GNU Autotools, changes handling of associated images, and
fixes OpenSlideView translation by large offsets.


## OpenSlide version 3.2.5, 2011-12-16

Version 3.2.5 has been released, supporting MIRAX 1.03 files, fixing
openslide_read_region for large dimensions, reducing memory usage,
disabling quickhash-1 for unusual TIFFs where it is very slow, and
fixing compilation errors.


## OpenSlide Python version 0.2.0, 2011-09-02

The first release of the Python bindings includes complete access to the
OpenSlide API, functionality for producing Deep Zoom images, and a simple
web application for displaying whole-slide images in a browser.


## OpenSlide version 3.2.4, 2011-03-07

Version 3.2.4 has been released, supporting MIRAX files without non-hierarchical sections,
working around some GKeyFile bugs, and fixing compilation errors on Windows.


## OpenSlide version 3.2.3, 2010-09-09

Version 3.2.3 has been released, supporting more MIRAX files, adding a background color
property, fixing some MIRAX drawing bugs, and adding support for quickhash-1 on all
platforms.


## OpenSlide Java version 0.9.2, 2010-08-10

Version 0.9.2 of the Java bindings removes some experimental CMU-specific annotation support.


## OpenSlide Java version 0.9.1, 2010-06-16

Version 0.9.1 of the Java bindings fixes a Windows build bug and removes checks for negative coordinates and zero dimensions.


## OpenSlide version 3.2.2, 2010-06-16

Version 3.2.2 has been released, adding support for negative coordinates and zero-sized dimensions in openslide_read_region, fixing a Windows build bug with new NGR support, and adding untested BigTIFF support.


## OpenSlide version 3.2.1, 2010-06-03

Version 3.2.1 has been released, fixing Windows crashes, quieting down the error logging, and fixing problems with libjpeg 7.


## OpenSlide Java version 0.9.0, 2010-06-01

Version 0.9.0 of the Java bindings adds support for the error handling system, eliminates the swig dependency, and adds new methods for painting.


## OpenSlide version 3.2.0, 2010-06-01

Version 3.2.0 has been released, adding experimental CMake support and fixes for building with MSVC, an error handling mechanism, initial Hamamatsu Nanozoomer VMU support, and the "openslide-write-png" tool.


## OpenSlide version 3.1.1, 2010-04-27

Version 3.1.1 has been released, fixing some bugs reading invalid VMS files. VMS files with multiple layers (NoLayers > 1) are also supported now, but the additional layers are ignored.


## OpenSlide version 3.1.0, 2010-04-01

Version 3.1.0 has been released, which fixes problems with some TIFF files and adds support for certain newer Aperio files (compression 33005).


## OpenSlide version 3.0.3, 2010-03-01

Version 3.0.3 has been released, which fixes nasty artifacts in some MIRAX files seen at some zoom levels.


## OpenSlide version 3.0.2, 2010-02-17

Version 3.0.2 has been released, which restores the ability to build with glib 2.12, at the expense of not having "quickhash-1" in that configuration.


## OpenSlide version 3.0.1, 2010-02-04

Version 3.0.1 has been released, with a fix for drawing the edges of TIFF files.


## OpenSlide Java version 0.8.0, 2010-01-28

Version 0.8.0 of the Java bindings changes the license to LGPLv2, fixes some bugs, adds a new selection type, and adds a call to paint a specific layer without scaling.


## OpenSlide version 3.0.0, 2010-01-28

Version 3.0.0 has been released, with a license change to LGPLv2, introduction of "quickhash-1", MIRAX bug fixes, and documentation improvements.

{% endif %}
