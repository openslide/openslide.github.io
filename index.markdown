---
layout: default
title: OpenSlide
---

<div markdown="1" class="newsflash">
{% include news.markdown %}
</div>

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