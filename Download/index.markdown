---
layout: default
title: Downloading OpenSlide

latest-version: 3.2.4
latest-version-java: 0.9.2
latest-version-python: 0.2.0
---

OpenSlide is available under the terms of the GNU Lesser General Public License, version 2.1.

Source
------

Source code is available for the following releases:

 * OpenSlide {{ page.latest-version }} (stable API)
   * [`openslide-{{ page.latest-version }}.tar.gz`][1]
   * [`openslide-{{ page.latest-version }}.tar.xz`][2]
 * OpenSlide Java interface {{ page.latest-version-java }} (still unstable API, subject to change)
   * [`openslide-java-{{ page.latest-version-java }}.tar.gz`][3]
   * [`openslide-java-{{ page.latest-version-java }}.tar.xz`][4]
 * OpenSlide Python interface {{ page.latest-version-python }} (still unstable API, subject to change)
   * [`openslide-python-{{ page.latest-version-python }}.tar.gz`][12]
   * [`openslide-python-{{ page.latest-version-python }}.tar.xz`][13]

[1]: http://github.com/downloads/openslide/openslide/openslide-{{ page.latest-version }}.tar.gz
[2]: http://github.com/downloads/openslide/openslide/openslide-{{ page.latest-version }}.tar.xz
[3]: http://github.com/downloads/openslide/openslide-java/openslide-java-{{ page.latest-version-java }}.tar.gz
[4]: http://github.com/downloads/openslide/openslide-java/openslide-java-{{ page.latest-version-java }}.tar.xz
[12]: http://github.com/downloads/openslide/openslide-python/openslide-python-{{ page.latest-version-python }}.tar.gz
[13]: http://github.com/downloads/openslide/openslide-python/openslide-python-{{ page.latest-version-python }}.tar.xz


Win32 Binaries
--------------
See the [Windows binaries label][5].
For now, here is a [temporary location][6].

[5]: http://github.com/openslide/openslide/issues/labels/Windows%20binaries
[6]: http://openslide.cs.cmu.edu/download/tmp/win32


Fedora
------
Fedora users can install OpenSlide with `yum install openslide`.

Red Hat Enterprise Linux / CentOS / Scientific Linux
----------------------------------------------------
After installing [EPEL][7], users of RHEL >=5 or RHEL-derived systems can just `yum install openslide`.

[7]: https://fedoraproject.org/wiki/EPEL


Python
------
An alternative Python binding to OpenSlide is available at:
<http://www.osc.edu/~kerwin/pyOpenSlide/>

Version Control
---------------
[Git][8] repositories for OpenSlide are available. The commands to clone are:

 * `git clone git://github.com/openslide/openslide.git` ([github][9])
 * `git clone git://github.com/openslide/openslide-java.git` ([github][10])
 * `git clone git://github.com/openslide/openslide-python.git` ([github][11])

[8]: http://git-scm.com/
[9]: http://github.com/openslide/openslide
[10]: http://github.com/openslide/openslide-java
[11]: http://github.com/openslide/openslide-python
