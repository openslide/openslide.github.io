---
layout: default
title: OpenSlide
news_show_extended: false
---

{% include links.markdown %}
{% include versions.markdown %}

<a href="https://github.com/openslide">
<img style="position: absolute; top: 0; right: 0; border: 0;"
src="https://s3.amazonaws.com/github/ribbons/forkme_right_green_007200.png"
alt="Fork me on GitHub">
</a>

<div markdown="1" class="newsflash">
{% include news.markdown %}
***
Older news is available [here][news].
</div>

OpenSlide is a C library that provides a simple interface to read
whole-slide images (also known as virtual slides). The current version
is {{ latest-version }}, released {{ latest-version-date }}.

Java and Python bindings are also available. The Java binding includes a
simple image viewer. The Python binding includes a [Deep Zoom][26]
generator and a simple web-based viewer.

[Download][download]

[26]: http://msdn.microsoft.com/en-us/library/cc645050%28VS.95%29.aspx

About OpenSlide
---------------

The library can read virtual slides in the following formats:

 * [Aperio (.svs, .tif)][format-aperio]
 * [Hamamatsu (.vms, .vmu)][format-hamamatsu]
 * [Leica (.scn)][format-leica]
 * [MIRAX (.mrxs)][format-mirax]
 * [Trestle (.tif)][format-trestle]
 * [Generic tiled TIFF (.tif)][format-generic-tiff]

It provides a simple C interface for programmers to use to decode
images of these kinds.

OpenSlide's support for these formats is not endorsed by their respective
vendors and may be incomplete.  Problems should be reported to the OpenSlide
[mailing list][users-subscribe] or [issue tracker][c-issues].

OpenSlide is a product of the research group of [M. Satyanarayanan][8]
(Satya) in the Carnegie Mellon [School of Computer Science][9].

[8]: http://www.cs.cmu.edu/~satya/
[9]: http://www.cs.cmu.edu/


See how [some projects use OpenSlide][other-projects].


Demo
----

There is a [web-based demo][demo] of OpenSlide rendering various slide
formats.


Mailing Lists
-------------

There are two mailing lists for OpenSlide:

 * Users mailing list. Once subscribed, anyone can post. This list is for asking questions about OpenSlide.
   * [Users list subscription info][users-subscribe]
   * [Users list archive][users-archive]

 * Announcement mailing list. It is a low-volume list and is moderated. All users are recommended to subscribe to this list.
   * [Announcement list subscription info][announce-subscribe]
   * [Announcement list archive][announce-archive]


Documentation
-------------

Some documentation is included within the downloadable files. Additionally there is:
 * [C API Documentation][api]
 * [Supported Virtual Slide Formats][formats]
 * [List of Known Properties][properties]
 * [Requested Properties][17]
 * [OpenSlide Wiki][wiki]

[17]: Requested%20Properties


Development
-----------

Development of OpenSlide happens on [GitHub][github]:

 * [OpenSlide][c-github] ([issue tracker][c-issues])
 * [OpenSlide Java][java-github] ([issue tracker][java-issues])
 * [OpenSlide Python][python-github] ([issue tracker][python-issues])
 * [Windows build scripts][winbuild-github] ([issue tracker][winbuild-issues])
 * [Website][site-github] ([issue tracker][site-issues])


Test Data
---------

Some freely-distributable test data is available via [HTTP][testdata] or
[rsync][testdata-rsync].


Tech Report
-----------

The architecture and design of the library is described in a technical report:

*A Vendor-Neutral Library and Viewer for Whole-Slide Images*  
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