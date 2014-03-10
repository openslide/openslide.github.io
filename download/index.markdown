---
layout: default
title: Downloading OpenSlide
releases:
  c:
    - {version: 3.4.0, date: 2014-01-25}
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
  python:
    - {version: 1.0.1, date: 2014-03-09}
    - {version: 1.0.0, date: 2014-03-09}
    - {version: 0.5.1, date: 2014-01-26}
    - {version: 0.5.0, date: 2014-01-25}
    - {version: 0.4.0, date: 2012-09-08}
    - {version: 0.3.0, date: 2011-12-16}
    - {version: 0.2.0, date: 2011-09-02}
  java:
    - {version: 0.12.0, date: 2014-01-25}
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
  winbuild:
    - {date: 2014-01-25}
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

#### OpenSlide Python interface (stable API)
{% assign package = 'openslide-python' %}
{% assign releases = page.releases.python %}
{% include source-release-table.markdown %}

#### OpenSlide Java interface (still unstable API, subject to change)
{% assign package = 'openslide-java' %}
{% assign releases = page.releases.java %}
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

Distribution Packages
---------------------

<table class="pinfo">
  <thead>
    <tr>
      <th rowspan="2">Platform</th>
      <th rowspan="2">Distribution</th>
      <th rowspan="2">OpenSlide</th>
      <th colspan="2">OpenSlide Python</th>
    </tr>
    <tr>
      <th>Python 2</th>
      <th>Python 3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Linux</th>
      <th><a href="http://fedoraproject.org/">Fedora</a></th>
      <td><code>yum install openslide</code></td>
      <td><code>yum install openslide-python</code></td>
      <td><code>yum install openslide-python3</code></td>
    </tr>
    <tr>
      <th>Linux</th>
      <th>
        <a href="http://www.debian.org/">Debian</a><br>
        <a href="http://www.ubuntu.com/">Ubuntu</a>
      </th>
      <td><code>apt-get install openslide-tools</code></td>
      <td>
        <code>apt-get install python-openslide</code><br>
        <i>(Debian</i> <code>unstable</code><i>, Ubuntu &ge; 14.04)</i>
      </td>
      <td>
        <code>apt-get install python3-openslide</code><br>
        <i>(Debian</i> <code>unstable</code><i>, Ubuntu &ge; 14.04)</i>
      </td>
    </tr>
    <tr>
      <th>Linux</th>
      <th>
        <a href="http://www.redhat.com/products/enterprise-linux/">Red Hat Enterprise Linux</a><br>
        <a href="https://www.centos.org/">CentOS</a><br>
        <a href="https://www.scientificlinux.org/">Scientific Linux</a>
      </th>
      <td>
        <i>First, install <a href="https://fedoraproject.org/wiki/EPEL">EPEL</a>.</i><br>
        <code>yum install openslide</code><br>
        <i>(RHEL/CentOS/Scientific Linux &ge; 5)</i>
      </td>
      <td>
        <i>First, install <a href="https://fedoraproject.org/wiki/EPEL">EPEL</a>.</i><br>
        <code>yum install openslide-python</code><br>
        <i>(RHEL/CentOS/Scientific Linux &ge; 7)</i>
      </td>
      <td></td>
    </tr>
    <tr>
      <th>Mac OS X</th>
      <th><a href="http://www.macports.org/">MacPorts</a></th>
      <td><code>port install openslide</code></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>Mac OS X</th>
      <th><a href="http://brew.sh/">Homebrew</a></th>
      <td><code>brew install openslide</code></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>Python</th>
      <th><a href="https://pypi.python.org/pypi">PyPI</a></th>
      <td></td>
      <td><code>pip install openslide-python</code></td>
      <td>
        <code>pip-python3 install openslide-python</code><br>
        <i>(or </i><code>pip-3.3</code><i>, </i><code>pip</code><i>, etc.)</i>
      </td>
    </tr>
  </tbody>
</table>


Version Control
---------------
[Git][git] repositories are available:

<table class="pinfo">
  <thead>
    <tr>
      <th>Repository</th>
      <th>Clone command</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th><a href="https://github.com/openslide/openslide">OpenSlide</a></th>
      <td><code>git clone https://github.com/openslide/openslide.git</code></td>
    </tr>
    <tr>
      <th><a href="https://github.com/openslide/openslide-python">OpenSlide Python</a></th>
      <td><code>git clone https://github.com/openslide/openslide-python.git</code></td>
    </tr>
    <tr>
      <th><a href="https://github.com/openslide/openslide-java">OpenSlide Java</a></th>
      <td><code>git clone https://github.com/openslide/openslide-java.git</code></td>
    </tr>
    <tr>
      <th><a href="https://github.com/openslide/openslide-winbuild">Windows build scripts</a></th>
      <td><code>git clone https://github.com/openslide/openslide-winbuild.git</code></td>
    </tr>
    <tr>
      <th><a href="https://github.com/openslide/openslide.github.com">Website</a></th>
      <td><code>git clone https://github.com/openslide/openslide.github.com.git</code></td>
    </tr>
  </tbody>
</table>

<!-- Ensure spacing above footer -->
<span></span>

[git]: http://git-scm.com/
