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

[1]: https://github.com/downloads/openslide/openslide/openslide-{{ latest-version }}.tar.gz
[2]: https://github.com/downloads/openslide/openslide/openslide-{{ latest-version }}.tar.xz
[3]: https://github.com/downloads/openslide/openslide-java/openslide-java-{{ latest-version-java }}.tar.gz
[4]: https://github.com/downloads/openslide/openslide-java/openslide-java-{{ latest-version-java }}.tar.xz
[12]: https://github.com/downloads/openslide/openslide-python/openslide-python-{{ latest-version-python }}.tar.gz
[13]: https://github.com/downloads/openslide/openslide-python/openslide-python-{{ latest-version-python }}.tar.xz


Windows Binaries
----------------

The latest build is dated {{ latest-version-winbuild }}:

 * [32-bit binaries][14]
 * [64-bit binaries][15]
 * [Corresponding sources][16]

Problems with these binaries can be reported [here][winbuild-issues].

[14]: https://github.com/downloads/openslide/openslide-winbuild/openslide-win32-{{ latest-version-winbuild }}.zip
[15]: https://github.com/downloads/openslide/openslide-winbuild/openslide-win64-{{ latest-version-winbuild }}.zip
[16]: https://github.com/downloads/openslide/openslide-winbuild/openslide-winbuild-{{ latest-version-winbuild }}.zip

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

Mac OS X
--------
OpenSlide is available from [MacPorts][macports] via
`port install openslide`.

[macports]: http://www.macports.org/

Version Control
---------------
[Git][8] repositories for OpenSlide are available. The commands to clone are:

 * `git clone git://github.com/openslide/openslide.git` ([GitHub][c-github])
 * `git clone git://github.com/openslide/openslide-java.git` ([GitHub][java-github])
 * `git clone git://github.com/openslide/openslide-python.git` ([GitHub][python-github])
 * `git clone git://github.com/openslide/openslide-winbuild.git` ([GitHub][winbuild-github])

[8]: http://git-scm.com/
