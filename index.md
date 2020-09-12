---
title: OpenSlide
classes: forkme
news_show_extended: false
extra_credits:
  <a href="https://github.com/aral/fork-me-on-github-retina-ribbons/">
  "Fork me on GitHub" ribbon</a> copyright &copy; 2013 Aral Balkan,
  released under a
  <a href="https://creativecommons.org/licenses/by/2.0/uk/">
  Creative Commons Attribution 2.0&#58; England & Wales</a> license.
---

{% include links.md %}

<a href="https://github.com/openslide">
  <img class="forkme-ribbon" src="/images/fork-me.png" alt="Fork me on GitHub">
</a>

<div markdown="1" class="newsflash">
{% include news.md %}
***
Older news is available [here][news].
</div>

OpenSlide is a C library that provides a simple interface to read
whole-slide images (also known as virtual slides). The current version
is {{ site.data.releases.c[0].version }}, released
{{ site.data.releases.c[0].date }}.

Python and Java bindings are also available. The Python binding includes a
[Deep Zoom][deepzoom] generator and a simple web-based viewer. The Java
binding includes a simple image viewer.

OpenSlide and its official language bindings are released under the
terms of the [GNU Lesser General Public License, version 2.1][lgplv2.1].

[Download][download]

[deepzoom]: http://msdn.microsoft.com/en-us/library/cc645050%28VS.95%29.aspx

About OpenSlide
---------------

The library can read virtual slides in the following formats:

 * [Aperio (.svs, .tif)][format-aperio]
 * [Hamamatsu (.vms, .vmu, .ndpi)][format-hamamatsu]
 * [Leica (.scn)][format-leica]
 * [MIRAX (.mrxs)][format-mirax]
 * [Philips (.tiff)][format-philips]
 * [Sakura (.svslide)][format-sakura]
 * [Trestle (.tif)][format-trestle]
 * [Ventana (.bif, .tif)][format-ventana]
 * [Generic tiled TIFF (.tif)][format-generic-tiff]

It provides a simple C interface for programmers to use to decode
images of these kinds.

OpenSlide's support for these formats is not endorsed by their respective
vendors and may be incomplete.  Problems should be reported to the OpenSlide
[mailing list][users-subscribe] or [issue tracker][c-issues].

OpenSlide is a product of the research group of [M. Satyanarayanan][satya]
(Satya) in the Carnegie Mellon University [School of Computer Science][cmucs].

[cmucs]: https://www.cs.cmu.edu/
[satya]: https://www.cs.cmu.edu/~satya/


See how [some projects use OpenSlide][other-projects].


Demo
----

There is a [web-based demo][demo] of OpenSlide rendering various slide
formats.


Documentation
-------------

Some documentation is included within the downloadable files.
Additionally there is:

 * [C API Documentation][c-api]
 * [Python API Documentation][python-api]
 * [Supported Virtual Slide Formats][formats]
 * [List of Known Properties][doc-properties]
 * [Using OpenSlide on Windows][doc-windows]
 * [Adding Support for a New Slide Format][doc-newformat]
 * [Debug Options][doc-debugopts]
 * [OpenSlide Wiki][wiki]


Getting Help
------------

First, try the search box at the top of the page.  It covers the OpenSlide
website, mailing list, issue tracker, and wiki.

Questions should be sent to the [users mailing list](#mailing-lists).  If
you think you have found a bug, please report it in the appropriate [issue
tracker](#development).


Mailing Lists
-------------

There are two mailing lists for OpenSlide:

 * Users mailing list. Once subscribed, anyone can post. This list is for asking questions about OpenSlide.
   * [Users list subscription info][users-subscribe]
   * [Users list archive][users-archive] (also available on [MARC][users-archive-marc])

 * Announcement mailing list. It is a low-volume list and is moderated. All users are recommended to subscribe to this list.
   * [Announcement list subscription info][announce-subscribe]
   * [Announcement list archive][announce-archive] (also available on [MARC][announce-archive-marc])


Development
-----------

Development of OpenSlide happens on [GitHub][github]:

 * [OpenSlide][c-github] ([issue tracker][c-issues])
 * [OpenSlide Python][python-github] ([issue tracker][python-issues])
 * [OpenSlide Java][java-github] ([issue tracker][java-issues])
 * [Windows build scripts][winbuild-github] ([issue tracker][winbuild-issues])
 * [Website][site-github] ([issue tracker][site-issues])
 * [Old Buildbot configuration][automation-github] ([issue tracker][automation-issues])


Test Data
---------

Some [freely-distributable test data][testdata] is available.


Publications
------------

The design and implementation of the library are described in a published
technical note:

*OpenSlide: A Vendor-Neutral Software Foundation for Digital Pathology*  
Adam Goode, Benjamin Gilbert, Jan Harkes, Drazen Jukic, M. Satyanarayanan  
Journal of Pathology Informatics 2013, 4:27  
[Abstract][paper-abstract]
[HTML][paper-html]
[PDF][paper-pdf]

There is also an older technical report:

*A Vendor-Neutral Library and Viewer for Whole-Slide Images*  
Adam Goode, M. Satyanarayanan  
Technical Report CMU-CS-08-136, June 2008  
Computer Science Department, Carnegie Mellon University  
[Abstract][tr-abstract]
[PDF][tr-full]

[paper-abstract]: http://www.jpathinformatics.org/article.asp?issn=2153-3539;year=2013;volume=4;issue=1;spage=27;epage=27;aulast=Goode;type=0
[paper-html]: http://www.jpathinformatics.org/article.asp?issn=2153-3539;year=2013;volume=4;issue=1;spage=27;epage=27;aulast=Goode
[paper-pdf]: http://download.openslide.org/docs/JPatholInform_2013_4_1_27_119005.pdf
[tr-abstract]: http://reports-archive.adm.cs.cmu.edu/anon/2008/abstracts/08-136.html
[tr-full]: http://reports-archive.adm.cs.cmu.edu/anon/2008/CMU-CS-08-136.pdf


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
OpenSlide has been supported by the [National Institutes of Health][nih] and the [Clinical and Translational Science Institute][ctsi] at the University of Pittsburgh.

[nih]: http://www.nih.gov/
[ctsi]: http://www.ctsi.pitt.edu/
