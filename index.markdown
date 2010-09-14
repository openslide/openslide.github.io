---
---
<!--
= OpenSlide =
{
#!NewsFlash
= OpenSlide Java version 0.9.2, 2010-08-10 =
Version 0.9.2 of the Java bindings removes some experimental CMU-specific annotation support.

= OpenSlide Java version 0.9.1, 2010-06-16 =
Version 0.9.1 of the Java bindings fixes a Windows build bug and removes checks for negative coordinates and zero dimensions.

= OpenSlide version 3.2.2, 2010-06-16 =
Version 3.2.2 has been released, adding support for negative coordinates and zero-sized dimensions in openslide_read_region, fixing a Windows build bug with new NGR support, and adding untested BigTIFF support.

= OpenSlide version 3.2.1, 2010-06-03 =
Version 3.2.1 has been released, fixing Windows crashes, quieting down the error logging, and fixing problems with libjpeg 7.

= OpenSlide Java version 0.9.0, 2010-06-01 =
Version 0.9.0 of the Java bindings adds support for the error handling system, eliminates the swig dependency, and adds new methods for painting.

= OpenSlide version 3.2.0, 2010-06-01 =
Version 3.2.0 has been released, adding experimental CMake support and fixes for building with MSVC, an error handling mechanism, initial Hamamatsu Nanozoomer VMU support, and the "openslide-write-png" tool.

= OpenSlide version 3.1.1, 2010-04-27 =
Version 3.1.1 has been released, fixing some bugs reading invalid VMS files. VMS files with multiple layers (NoLayers > 1) are also supported now, but the additional layers are ignored.

= OpenSlide version 3.1.0, 2010-04-01 =
Version 3.1.0 has been released, which fixes problems with some TIFF files and adds support for certain newer Aperio files (compression 33005).

= OpenSlide version 3.0.3, 2010-03-01 =
Version 3.0.3 has been released, which fixes nasty artifacts in some MIRAX files seen at some zoom levels.

= OpenSlide version 3.0.2, 2010-02-17 =
Version 3.0.2 has been released, which restores the ability to build with glib 2.12, at the expense of not having "quickhash-1" in that configuration.

= OpenSlide version 3.0.1, 2010-02-04 =
Version 3.0.1 has been released, with a fix for drawing the edges of TIFF files.

= OpenSlide Java version 0.8.0, 2010-01-28 =
Version 0.8.0 of the Java bindings changes the license to LGPLv2, fixes some bugs, adds a new selection type, and adds a call to paint a specific layer without scaling.

= OpenSlide version 3.0.0, 2010-01-28 =
Version 3.0.0 has been released, with a license change to LGPLv2, introduction of "quickhash-1", MIRAX bug fixes, and documentation improvements.


}
-->
OpenSlide
=========

OpenSlide is a C library that provides a simple interface to read
whole-slide images (also known as virtual slides). The current version
is 3.2.2, released 2010-06-16. There is also a Java binding available,
including a simple image viewer.

[Download][1]

[1]: Download

About OpenSlide
---------------

The library can read virtual slides in the following formats:

 * [Trestle (.tif)][2]
 * [Hamamatsu (.vms, .vmu)][3]
 * [Aperio (.svs, .tif)][4]
 * [MIRAX (.mrxs)][5]
 * [Generic tiled TIFF (.tif)][6]

[2]: Trestle%20format
[3]: Hamamatsu%20format
[4]: Aperio%20format
[5]: MIRAX%20format
[6]: Generic%20tiled%20TIFF%20format

It provides a simple C interface for programmers to use to decode
images of these kinds.

See [Supported Virtual Slide Formats][7] for more information.

[7]: Supported%20Virtual%20Slide%20Formats


OpenSlide is a product of the research group of [M. Satyanarayanan][8]
(Satya) in the Carnegie Mellon [School of Computer Science][9].

[8]: http://www.cs.cmu.edu/~satya/
[9]: http://www.cs.cmu.edu/


See how [some projects use OpenSlide][10].

[10]: Some%20Projects%20Using%20OpenSlide


Mailing Lists
-------------

There are two mailing lists for OpenSlide:

 * Users mailing list. Once subscribed, anyone can post. This list is for asking questions about OpenSlide.
   * [Users list subscription info][11]
   * [Users list archive][12]

 * Announcement mailing list. It is a low-volume list and is moderated. All users are recommended to subscribe to this list.
   * [Announcement list subscription info][13]
   * [Announcement list archive][14]

[11]: http://lists.andrew.cmu.edu/mailman/listinfo/openslide-users/
[12]: http://lists.andrew.cmu.edu/pipermail/openslide-users/
[13]: http://lists.andrew.cmu.edu/mailman/listinfo/openslide-announce/
[14]: http://lists.andrew.cmu.edu/pipermail/openslide-announce/


Documentation
-------------

Some documentation is included within the downloadable files. Additionally there is:
 * [C API Documentation][15]
 * [List of Known Properties][16]
 * [Requested Properties][17]

[15]: api/openslide_8h.html
[16]: List%20of%20Known%20Properties
[17]: Requested%20Properties


Test Data
---------

Some [freely-distributable test data][18] is available.

[18]: http://openslide.cs.cmu.edu/download/openslide-testdata.torrent


Tech Report
-----------

The architecture and design of the library is described in a technical report:

"A Vendor-Neutral Library and Viewer for Whole-Slide Images"  
Adam Goode, M. Satyanarayanan  
Technical Report CMU-CS-08-136, June 2008  
Computer Science Department, Carnegie Mellon University  
[Abstract][19]
[PDF][20]

[19]: http://reports-archive.adm.cs.cmu.edu/anon/2008/abstracts/08-136.html
[20]: http://reports-archive.adm.cs.cmu.edu/anon/2008/CMU-CS-08-136.pdf


About whole-slide images
------------------------

Whole-slide images, also known as virtual slides, are large, high resolution images used in digital
pathology. Reading these images using standard image tools or libraries is a challenge because
these tools are typically designed for images that can comfortably be uncompressed into RAM or
a swap file. Whole-slide images routinely exceed RAM sizes, often occupying tens of gigabytes
when uncompressed. Additionally, whole-slide images are typically multi-resolution, and only a
small amount of image data might be needed at a particular resolution.

There is no universal data format for whole-slide images, so each vendor implements its own
formats, libraries, and viewers. Vendors typically do not document their formats. Even when
there is documentation, important details are omitted. Because a vendor’s library or viewer is the
only way to view a particular whole-slide image, doctors and researchers can be unnecessarily
tied to a particular vendor. Finally, few (if any) vendors provide libraries and viewers for non-Windows platforms. Some have gone with a server approach, pushing tiles through a web server,
or using Java applets, but these approaches have shortcomings in high-latency or non-networked
environments.

Acknowledgements
----------------
OpenSlide has been supported by the [National Institutes of Health][21] and the [Clinical and Translational Science Institute][22] at the University of Pittsburgh.

[21]: http://www.nih.gov/
[22]: http://www.ctsi.pitt.edu/


[![NIH logo](images/NIH_logo.png)][21]
