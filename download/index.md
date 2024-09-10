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


## Binaries

Problems with these binaries can be reported [here][bin-issues].
If you're looking for the bleeding edge,
[nightly development builds][snapshots] are also available.

<div class="releases">
  <table>
    {% for release in site.data.releases.bin %}
      {% if release.version %}
        {% assign version = release.version %}
      {% else %}
        {% capture version %}{{ release.date|remove:'-' }}{% endcapture %}
      {% endif %}
      <tr class="{% cycle 'bin': 'odd', 'even' %}">
        <th>
          <a href="https://github.com/openslide/openslide-bin/releases/tag/v{{ version }}">
            {{ version }}
          </a>
        </th>
        <td>{{ release.date }}</td>
        {% if release.version %}
          <td><a href="https://github.com/openslide/openslide-bin/releases/download/v{{ version }}/openslide-bin-{{ version }}.tar.gz">Source</a></td>
          <td><a href="https://github.com/openslide/openslide-bin/releases/download/v{{ version }}/openslide-bin-{{ version }}-linux-x86_64.tar.xz">Linux x86_64</a></td>
          <td>{% if release.linux_aarch64 %}<a href="https://github.com/openslide/openslide-bin/releases/download/v{{ version }}/openslide-bin-{{ version }}-linux-aarch64.tar.xz">Linux aarch64</a>{% endif %}</td>
          <td><a href="https://github.com/openslide/openslide-bin/releases/download/v{{ version }}/openslide-bin-{{ version }}-macos-arm64-x86_64.tar.xz">macOS</a></td>
          <td></td>
          <td><a href="https://github.com/openslide/openslide-bin/releases/download/v{{ version }}/openslide-bin-{{ version }}-windows-x64.zip">Windows x64</a></td>
        {% else %}
          <td><a href="https://github.com/openslide/openslide-bin/releases/download/v{{ version }}/openslide-winbuild-{{ version }}.zip">Source</a></td>
          <td></td>
          <td></td>
          <td></td>
          <td><a href="https://github.com/openslide/openslide-bin/releases/download/v{{ version }}/openslide-win32-{{ version }}.zip">Windows x86</a></td>
          <td><a href="https://github.com/openslide/openslide-bin/releases/download/v{{ version }}/openslide-win64-{{ version }}.zip">Windows x64</a></td>
        {% endif %}
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
      <th>Any</th>
      <th><a href="https://conan.io/">Conan</a></th>
      <td>
        <i>Add to</i> <code>conanfile.txt</code>:
        <pre>[requires]
openslide/[~4]</pre>
      </td>
      <td></td>
    </tr>
    <tr>
      <th>FreeBSD</th>
      <th><a href="https://ports.freebsd.org/">Ports</a></th>
      <td><code>pkg install openslide</code></td>
      <td><code>pkg install py311-openslide-python</code></td>
    </tr>
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
      <th><a href="https://spack.io/">Spack</a></th>
      <td><code>spack install openslide</code></td>
      <td><code>spack install py-openslide-python</code></td>
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
      <td><code>port install py312-openslide</code></td>
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
      <th><a href="https://github.com/openslide/openslide-bin">Binary builds</a></th>
      <td><code>git clone https://github.com/openslide/openslide-bin.git</code></td>
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
