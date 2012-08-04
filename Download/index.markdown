---
layout: default
title: Downloading OpenSlide
---

{% include links.markdown %}
{% include versions.markdown %}

OpenSlide is available under the terms of the GNU Lesser General Public License, version 2.1.

Source
------

Source code is available for the following releases:

 * OpenSlide {{ latest-version }} (stable API)
   * [`openslide-{{ latest-version }}.tar.gz`][1]
   * [`openslide-{{ latest-version }}.tar.xz`][2]
 * OpenSlide Java interface {{ latest-version-java }} (still unstable API, subject to change)
   * [`openslide-java-{{ latest-version-java }}.tar.gz`][3]
   * [`openslide-java-{{ latest-version-java }}.tar.xz`][4]
 * OpenSlide Python interface {{ latest-version-python }} (still unstable API, subject to change)
   * [`openslide-python-{{ latest-version-python }}.tar.gz`][12]
   * [`openslide-python-{{ latest-version-python }}.tar.xz`][13]

[1]: http://github.com/downloads/openslide/openslide/openslide-{{ latest-version }}.tar.gz
[2]: http://github.com/downloads/openslide/openslide/openslide-{{ latest-version }}.tar.xz
[3]: http://github.com/downloads/openslide/openslide-java/openslide-java-{{ latest-version-java }}.tar.gz
[4]: http://github.com/downloads/openslide/openslide-java/openslide-java-{{ latest-version-java }}.tar.xz
[12]: http://github.com/downloads/openslide/openslide-python/openslide-python-{{ latest-version-python }}.tar.gz
[13]: http://github.com/downloads/openslide/openslide-python/openslide-python-{{ latest-version-python }}.tar.xz


Win32 Binaries
--------------
See the [Windows binaries label][5].

[5]: http://github.com/openslide/openslide/issues/labels/Windows%20binaries


Fedora
------
Fedora users can install OpenSlide with `yum install openslide`.

Debian/Ubuntu
-------------
Users of Ubuntu and Debian testing can install OpenSlide and its command-line
utilities with `apt-get install openslide-tools`.

Red Hat Enterprise Linux / CentOS / Scientific Linux
----------------------------------------------------
After installing [EPEL][7], users of RHEL >=5 or RHEL-derived systems can just `yum install openslide`.

[7]: https://fedoraproject.org/wiki/EPEL

Version Control
---------------
[Git][8] repositories for OpenSlide are available. The commands to clone are:

 * `git clone git://github.com/openslide/openslide.git` ([GitHub][c-github])
 * `git clone git://github.com/openslide/openslide-java.git` ([GitHub][java-github])
 * `git clone git://github.com/openslide/openslide-python.git` ([GitHub][python-github])

[8]: http://git-scm.com/
