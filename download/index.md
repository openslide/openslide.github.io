---
title: Downloading OpenSlide
permalink: /download/
redirect_from:
  - /Download/
---

{% include links.md %}

OpenSlide and its official language bindings are available under the terms
of the [GNU Lesser General Public License, version 2.1][lgplv2.1].

Source
------

#### OpenSlide (stable API)
{% assign package = 'openslide' %}
{% assign releases = site.data.releases.c %}
{% include source-release-table.md %}

#### OpenSlide Python interface (stable API)
{% assign package = 'openslide-python' %}
{% assign releases = site.data.releases.python %}
{% include source-release-table.md %}

#### OpenSlide Java interface (still unstable API, subject to change)
{% assign package = 'openslide-java' %}
{% assign releases = site.data.releases.java %}
{% include source-release-table.md %}

Windows Binaries
----------------

Problems with these binaries can be reported [here][winbuild-issues].

<div class="releases">
  <table>
    {% for release in site.data.releases.winbuild %}
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
      <th><a href="https://fedoraproject.org/">Fedora</a></th>
      <td><code>dnf install openslide</code></td>
      <td></td>
      <td><code>dnf install python3-openslide</code></td>
    </tr>
    <tr>
      <th>Linux</th>
      <th>
        <a href="https://www.debian.org/">Debian</a><br>
        <a href="http://www.ubuntu.com/">Ubuntu</a>
      </th>
      <td><code>apt-get install openslide-tools</code></td>
      <td>
        <code>apt-get install python-openslide</code><br>
      </td>
      <td>
        <code>apt-get install python3-openslide</code><br>
      </td>
    </tr>
    <tr>
      <th>Linux</th>
      <th><a href="https://www.opensuse.org/">openSUSE</a></th>
      <td><code>zypper install openslide-tools</code></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>Linux</th>
      <th>
        <a href="https://www.redhat.com/products/enterprise-linux/">Red Hat Enterprise Linux</a><br>
        <a href="https://www.centos.org/">CentOS</a><br>
        <a href="https://www.scientificlinux.org/">Scientific Linux</a>
      </th>
      <td>
        <i>First, install <a href="https://fedoraproject.org/wiki/EPEL">EPEL</a>.</i><br>
        <code>yum install openslide</code><br>
        <i>(RHEL/CentOS/Scientific Linux &ge; 6)</i>
      </td>
      <td>
        <i>First, install <a href="https://fedoraproject.org/wiki/EPEL">EPEL</a>.</i><br>
        <code>yum install openslide-python</code><br>
        <i>(RHEL/CentOS/Scientific Linux 7)</i>
      </td>
      <td>
        <i>First, install <a href="https://fedoraproject.org/wiki/EPEL">EPEL</a>.</i><br>
        <code>yum install python3-openslide</code><br>
        <i>(RHEL/CentOS Stream &ge; 8)</i>
      </td>
    </tr>
    <tr>
      <th>Mac OS X</th>
      <th><a href="https://www.macports.org/">MacPorts</a></th>
      <td><code>port install openslide</code></td>
      <td><code></code></td>
      <td><code>port install py39-openslide</code></td>
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
        <i>(or </i><code>pip-3.6</code><i>, </i><code>pip</code><i>, etc.)</i>
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
      <th><a href="https://github.com/openslide/openslide.github.io">Website</a></th>
      <td><code>git clone https://github.com/openslide/openslide.github.io.git</code></td>
    </tr>
    <tr>
      <th><a href="https://github.com/openslide/openslide-automation">Old Buildbot configuration</a></th>
      <td><code>git clone https://github.com/openslide/openslide-automation.git</code></td>
    </tr>
  </tbody>
</table>

<!-- Ensure spacing above footer -->
<span></span>

[git]: https://git-scm.com/
