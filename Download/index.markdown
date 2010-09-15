---
layout: default
title: Downloading OpenSlide

latest-version: 3.2.3
latest-version-java: 0.9.2
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

[1]: http://github.com/downloads/openslide/openslide/openslide-{{ page.latest-version }}.tar.gz
[2]: http://github.com/downloads/openslide/openslide/openslide-{{ page.latest-version }}.tar.xz
[3]: http://github.com/downloads/openslide/openslide-java/openslide-java-{{ page.latest-version-java }}.tar.gz
[4]: http://github.com/downloads/openslide/openslide-java/openslide-java-{{ page.latest-version-java }}.tar.xz


Win32 Binaries
--------------
See the [Win32 binaries label][5].
For now, here is a [temporary location][6].

[5]: http://github.com/openslide/openslide/issues/labels/win32-binaries
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
There is an OpenSlide binding for Python available at:
<http://www.osc.edu/~kerwin/pyOpenSlide/>

Version Control
---------------
[Git][8] repositories for OpenSlide are available. The commands to clone are:

 * `git clone git://github.com/openslide/openslide.git` ([github][9])
 * `git clone git://github.com/openslide/openslide-java.git` ([github][10])

[8]: http://git.or.cz/
[9]: http://github.com/openslide/openslide
[10]: http://github.com/openslide/openslide-java
