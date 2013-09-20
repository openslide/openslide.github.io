---
layout: default
title: Downloading OpenSlide
releases:
  c:
    - {version: 3.3.3, date: 2013-04-13}
    - {version: 3.3.2, date: 2012-12-01}
    - {version: 3.3.1, date: 2012-10-14}
    - {version: 3.3.0, date: 2012-09-08}
    - {version: 3.2.6, date: 2012-02-23}
    - {version: 3.2.5, date: 2011-12-16}
    - {version: 3.2.4, date: 2011-03-07}
    - {version: 3.2.3, date: 2010-09-09}
    - {version: 3.2.2, date: 2010-06-16}
    - {version: 3.2.1, date: 2010-06-03}
    - {version: 3.2.0, date: 2010-06-01}
    - {version: 3.1.1, date: 2010-04-27}
    - {version: 3.1.0, date: 2010-04-01}
    - {version: 3.0.3, date: 2010-03-01}
    - {version: 3.0.2, date: 2010-02-17}
    - {version: 3.0.1, date: 2010-02-04}
    - {version: 3.0.0, date: 2010-01-28}
    - {version: 2.3.1, date: 2009-12-14}
    - {version: 2.3.0, date: 2009-12-11}
    - {version: 2.2.1, date: 2009-10-23}
    - {version: 2.2.0, date: 2009-09-15}
    - {version: 2.1.0, date: 2009-08-18, no_xz: 1}
    - {version: 2.0.0, date: 2009-07-16, no_xz: 1}
  java:
    - {version: 0.11.0, date: 2012-09-08}
    - {version: 0.10.0, date: 2011-12-16}
    - {version: 0.9.2, date: 2010-08-10}
    - {version: 0.9.1, date: 2010-06-16}
    - {version: 0.9.0, date: 2010-06-01}
    - {version: 0.8.0, date: 2010-01-28}
    - {version: 0.7.2, date: 2009-12-09}
    - {version: 0.7.1, date: 2009-11-19}
    - {version: 0.7.0, date: 2009-09-15}
    - {version: 0.6.1, date: 2009-08-25, no_xz: 1}
    - {version: 0.6.0, date: 2009-08-17, no_xz: 1}
    - {version: 0.5.0, date: 2009-07-15, no_xz: 1}
  python:
    - {version: 0.4.0, date: 2012-09-08}
    - {version: 0.3.0, date: 2011-12-16}
    - {version: 0.2.0, date: 2011-09-02}
  winbuild:
    - {date: 2013-07-27}
    - {date: 2013-04-13}
    - {date: 2012-12-01}
    - {date: 2012-10-14}
    - {date: 2012-09-08}
    - {date: 2012-08-02}
---

{% include links.markdown %}

OpenSlide and its official language bindings are available under the terms
of the [GNU Lesser General Public License, version 2.1][lgplv2.1].

Source
------

#### OpenSlide (stable API)
{% assign package = 'openslide' %}
{% assign releases = page.releases.c %}
{% include source-release-table.markdown %}

#### OpenSlide Java interface (still unstable API, subject to change)
{% assign package = 'openslide-java' %}
{% assign releases = page.releases.java %}
{% include source-release-table.markdown %}

#### OpenSlide Python interface (still unstable API, subject to change)
{% assign package = 'openslide-python' %}
{% assign releases = page.releases.python %}
{% include source-release-table.markdown %}

Windows Binaries
----------------

Problems with these binaries can be reported [here][winbuild-issues].
If you're looking for the bleeding edge,
[nightly development builds][snapshots-windows] are also available.

<div class="releases">
  <table>
    {% for release in page.releases.winbuild %}
      <tr class="{% cycle 'winbuild': 'odd', 'even' %}">
        <th>{{ release.date }}</th>
        <td><a href="https://github.com/openslide/openslide-winbuild/releases/download/v{{ release.date|remove:'-' }}/openslide-win32-{{ release.date|remove:'-' }}.zip">32-bit</a></td>
        <td><a href="https://github.com/openslide/openslide-winbuild/releases/download/v{{ release.date|remove:'-' }}/openslide-win64-{{ release.date|remove:'-' }}.zip">64-bit</a></td>
        <td><a href="https://github.com/openslide/openslide-winbuild/releases/download/v{{ release.date|remove:'-' }}/openslide-winbuild-{{ release.date|remove:'-' }}.zip">Corresponding sources</a></td>
      </tr>
    {% endfor %}
  </table>
</div>

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
`port install openslide` and from [Homebrew][homebrew] via
`brew install openslide`.

[macports]: http://www.macports.org/
[homebrew]: http://mxcl.github.com/homebrew/

Version Control
---------------
[Git][8] repositories for OpenSlide are available. The commands to clone are:

 * `git clone git://github.com/openslide/openslide.git` ([GitHub][c-github])
 * `git clone git://github.com/openslide/openslide-java.git` ([GitHub][java-github])
 * `git clone git://github.com/openslide/openslide-python.git` ([GitHub][python-github])
 * `git clone git://github.com/openslide/openslide-winbuild.git` ([GitHub][winbuild-github])

[8]: http://git-scm.com/
