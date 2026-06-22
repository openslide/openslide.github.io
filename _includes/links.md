[news]: {{ site.baseurl }}/news/
[download]: {{ site.baseurl }}/download/
[download-bin]: {{ site.baseurl }}/download/#binaries
[download-copr]: https://copr.fedorainfracloud.org/coprs/g/openslide/openslide/
[download-ppa]: https://launchpad.net/~openslide/+archive/ubuntu/openslide
[download-pypi]: https://pypi.org/project/openslide-python/#files
[license]: {{ site.baseurl }}/license/
[demo]: {{ site.baseurl }}/demo/
[other-projects]: {{ site.baseurl }}/other-projects/
[github]: https://github.com/openslide
[wiki]: https://github.com/openslide/openslide/wiki
[testdata]: https://openslide.cs.cmu.edu/download/openslide-testdata/
[snapshots]: {{ site.baseurl }}/builds/
[submit-sample]: {{ site.baseurl }}/submit/

[doc-dev]: {{ site.baseurl }}/#development
[doc-debugopts]: {{ site.baseurl }}/docs/debugopts/
[doc-devguide]: {{ site.baseurl }}/docs/devguide/
[doc-newformat]: {{ site.baseurl }}/docs/newformat/
[doc-premultiplied]: {{ site.baseurl }}/docs/premultiplied-argb/
[doc-properties]: {{ site.baseurl }}/docs/properties/
[doc-signoff]: {{ site.baseurl }}/docs/signoff/
[doc-testsuite]: {{ site.baseurl }}/docs/testsuite/
[doc-windows]: {{ site.baseurl }}/docs/windows/
[gerror-rules]: https://docs.gtk.org/glib/error-reporting.html#rules-for-use-of-gerror

[c-api]: {{ site.baseurl }}/api/openslide_8h.html
[python-api]: {{ site.baseurl }}/api/python/

[formats]: {{ site.baseurl }}/formats/
[format-aperio]: {{ site.baseurl }}/formats/aperio/
[format-argos]: {{ site.baseurl }}/formats/argos/
[format-dicom]: {{ site.baseurl }}/formats/dicom/
[format-generic-tiff]: {{ site.baseurl }}/formats/generic-tiff/
[format-hamamatsu]: {{ site.baseurl }}/formats/hamamatsu/
[format-huron]: {{ site.baseurl }}/formats/huron/
[format-leica]: {{ site.baseurl }}/formats/leica/
[format-mirax]: {{ site.baseurl }}/formats/mirax/
[format-philips]: {{ site.baseurl }}/formats/philips/
[format-sakura]: {{ site.baseurl }}/formats/sakura/
[format-trestle]: {{ site.baseurl }}/formats/trestle/
[format-ventana]: {{ site.baseurl }}/formats/ventana/
[format-zeiss]: {{ site.baseurl }}/formats/zeiss/

[announce-subscribe]: https://lists.andrew.cmu.edu/mailman/listinfo/openslide-announce/
[users-subscribe]: https://lists.andrew.cmu.edu/mailman/listinfo/openslide-users/
[announce-archive]: https://lists.andrew.cmu.edu/pipermail/openslide-announce/
[users-archive]: https://lists.andrew.cmu.edu/pipermail/openslide-users/
[announce-archive-marc]: https://marc.info/?l=openslide-announce
[users-archive-marc]: https://marc.info/?l=openslide-users

[c-github]: https://github.com/openslide/openslide
[python-github]: https://github.com/openslide/openslide-python
[java-github]: https://github.com/openslide/openslide-java
[bin-github]: https://github.com/openslide/openslide-bin
[builds-github]: https://github.com/openslide/builds
[site-github]: https://github.com/openslide/openslide.github.io

[c-issues]: https://github.com/openslide/openslide/issues
[python-issues]: https://github.com/openslide/openslide-python/issues
[java-issues]: https://github.com/openslide/openslide-java/issues
[bin-issues]: https://github.com/openslide/openslide-bin/issues
[builds-issues]: https://github.com/openslide/builds/issues
[site-issues]: https://github.com/openslide/openslide.github.io/issues

[bin-pypi]: https://pypi.org/project/openslide-bin/

{% assign table = 'c' %}
{% include release-links.md %}
{% assign table = 'python' %}
{% include release-links.md %}
{% assign table = 'java' %}
{% include release-links.md %}
{% assign table = 'bin' %}
{% include release-links.md %}
