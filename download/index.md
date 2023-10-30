---
title: Downloading OpenSlide
permalink: /download/
redirect_from:
  - /Download/
---

{% include links.md %}

OpenSlide and its official language bindings are available under the terms
of the [GNU Lesser General Public License, version 2.1][license].

## Source

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


## Windows Binaries

Problems with these binaries can be reported [here][winbuild-issues].
If you're looking for the bleeding edge,
[nightly development builds][snapshots] are also available.

<div class="releases">
  <table>
    {% for release in site.data.releases.winbuild %}
      <tr class="{% cycle 'winbuild': 'odd', 'even' %}">
        <th>
          <a href="https://github.com/openslide/openslide-winbuild/releases/tag/v{{ release.date|remove:'-' }}">
            {{ release.date }}
          </a>
        </th>
        <td><a href="https://github.com/openslide/openslide-winbuild/releases/download/v{{ release.date|remove:'-' }}/openslide-win32-{{ release.date|remove:'-' }}.zip">32-bit</a></td>
        <td><a href="https://github.com/openslide/openslide-winbuild/releases/download/v{{ release.date|remove:'-' }}/openslide-win64-{{ release.date|remove:'-' }}.zip">64-bit</a></td>
        <td><a href="https://github.com/openslide/openslide-winbuild/releases/download/v{{ release.date|remove:'-' }}/openslide-winbuild-{{ release.date|remove:'-' }}.zip">Corresponding sources</a></td>
      </tr>
    {% endfor %}
  </table>
</div>


## Distribution Packages

<table class="pinfo">
  <thead>
    <tr>
      <th>Platform</th>
      <th>Distribution</th>
      <th>OpenSlide</th>
      <th>OpenSlide Python</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Linux</th>
      <th>
        <a href="https://almalinux.org/">AlmaLinux</a><br>
        <a href="https://www.centos.org/centos-stream/">CentOS Stream</a><br>
        <a href="https://www.oracle.com/linux/">Oracle Linux</a><br>
        <a href="https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux">Red Hat Enterprise Linux</a><br>
        <a href="https://rockylinux.org/">Rocky Linux</a>
      </th>
      <td>
        <div>
          <i>Official packages:</i><br>
          <b><i>First, install <a href="https://fedoraproject.org/wiki/EPEL">EPEL</a>.</i></b><br>
          <code>dnf install openslide-tools</code><br>
        </div>
        <div>
          <i>Latest OpenSlide:</i><br>
          <b><i>First, install <a href="https://fedoraproject.org/wiki/EPEL">EPEL</a>.</i></b><br>
          <code>
            dnf install dnf-plugins-core<br>
            dnf copr enable <a href="https://copr.fedorainfracloud.org/coprs/g/openslide/openslide/">@openslide/openslide</a><br>
            dnf install openslide-tools
          </code>
        </div>
      </td>
      <td>
        <div>
          <i>Official packages:</i><br>
          <b><i>First, install <a href="https://fedoraproject.org/wiki/EPEL">EPEL</a>.</i></b><br>
          <code>dnf install python3-openslide</code><br>
        </div>
        <div>
          <i>Latest OpenSlide Python:</i><br>
          <b><i>First, install <a href="https://fedoraproject.org/wiki/EPEL">EPEL</a>.</i></b><br>
          <code>
            dnf install dnf-plugins-core<br>
            dnf copr enable <a href="https://copr.fedorainfracloud.org/coprs/g/openslide/openslide/">@openslide/openslide</a><br>
            dnf install python3-openslide
          </code>
        </div>
      </td>
    </tr>
    <tr>
      <th>Linux</th>
      <th><a href="https://archlinux.org/">Arch Linux</a></th>
      <td><code>pacman -S openslide</code></td>
      <td></td>
    </tr>
    <tr>
      <th>Linux</th>
      <th><a href="https://www.debian.org/">Debian</a></th>
      <td><code>apt install openslide-tools</code></td>
      <td><code>apt install python3-openslide</code></td>
    </tr>
    <tr>
      <th>Linux</th>
      <th><a href="https://fedoraproject.org/">Fedora</a></th>
      <td>
        <div>
          <i>Official packages:</i><br>
          <code>dnf install openslide-tools</code>
        </div>
        <div>
          <i>Latest OpenSlide:</i><br>
          <code>
            dnf install dnf-plugins-core<br>
            dnf copr enable <a href="https://copr.fedorainfracloud.org/coprs/g/openslide/openslide/">@openslide/openslide</a><br>
            dnf install openslide-tools
          </code>
        </div>
      </td>
      <td>
        <div>
          <i>Official packages:</i><br>
          <code>dnf install python3-openslide</code>
        </div>
        <div>
          <i>Latest OpenSlide Python:</i><br>
          <code>
            dnf install dnf-plugins-core<br>
            dnf copr enable <a href="https://copr.fedorainfracloud.org/coprs/g/openslide/openslide/">@openslide/openslide</a><br>
            dnf install python3-openslide
          </code>
        </div>
      </td>
    </tr>
    <tr>
      <th>Linux</th>
      <th><a href="https://www.opensuse.org/">openSUSE</a></th>
      <td><code>zypper install openslide-tools</code></td>
      <td></td>
    </tr>
    <tr>
      <th>Linux</th>
      <th><a href="https://ubuntu.com/">Ubuntu</a></th>
      <td>
        <div>
          <i>Official packages:</i><br>
          <code>apt install openslide-tools</code>
        </div>
        <div>
          <i>Latest OpenSlide:</i><br>
          <code>
            apt install software-properties-common<br>
            add-apt-repository <a href="https://launchpad.net/~openslide/+archive/ubuntu/openslide">ppa:openslide/openslide</a><br>
            apt install openslide-tools
          </code>
        </div>
      </td>
      <td>
        <div>
          <i>Official packages:</i><br>
          <code>apt install python3-openslide</code>
        </div>
        <div>
          <i>Latest OpenSlide Python:</i><br>
          <code>
            apt install software-properties-common<br>
            add-apt-repository <a href="https://launchpad.net/~openslide/+archive/ubuntu/openslide">ppa:openslide/openslide</a><br>
            apt install python3-openslide
          </code>
        </div>
      </td>
    </tr>
    <tr>
      <th>macOS</th>
      <th><a href="https://brew.sh/">Homebrew</a></th>
      <td><code>brew install openslide</code></td>
      <td></td>
    </tr>
    <tr>
      <th>macOS</th>
      <th><a href="https://www.macports.org/">MacPorts</a></th>
      <td><code>port install openslide</code></td>
      <td><code>port install py311-openslide</code></td>
    </tr>
    <tr>
      <th>Python</th>
      <th><a href="https://conda-forge.org/">conda-forge</a></th>
      <td><code>conda install openslide</code></td>
      <td><code>conda install openslide-python</code></td>
    </tr>
    <tr>
      <th>Python</th>
      <th><a href="https://pypi.org/">PyPI</a></th>
      <td></td>
      <td><code>python3 -m pip install openslide-python</code></td>
    </tr>
    <tr>
      <th>Windows</th>
      <th><a href="https://www.msys2.org/">MSYS2</a></th>
      <td>
        <code>pacman -S mingw-w64-x86_64-openslide</code><br>
        <i>(or <a href="https://packages.msys2.org/base/mingw-w64-openslide">other variants</a>)</i>
      </td>
      <td></td>
    </tr>
    <tr>
      <th>Windows</th>
      <th><a href="https://vcpkg.io/">vcpkg</a></th>
      <td><code>vcpkg install openslide</code></td>
      <td></td>
    </tr>
  </tbody>
</table>


## Version Control

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
      <th><a href="https://github.com/openslide/builds">Nightly build infrastructure</a></th>
      <td><code>git clone https://github.com/openslide/builds.git</code></td>
    </tr>
    <tr>
      <th><a href="https://github.com/openslide/openslide.github.io">Website</a></th>
      <td><code>git clone https://github.com/openslide/openslide.github.io.git</code></td>
    </tr>
  </tbody>
</table>

<!-- Ensure spacing above footer -->
<span></span>

[git]: https://git-scm.com/
