---
title: Developer Guide
---

{% include links.md %}

For now, the main developer documentation is the
[Adding a New Format][doc-newformat] page.  Take particular note of the
section on error handling, but the entire page is worth reading.

The [other developer docs][doc-dev] may also be useful.


## Original development guide

_This section contains the original development guide written by Adam Goode
in 2010, with some updates by Benjamin Gilbert in 2012 and 2013.  It's no
longer actively maintained, but there's still some wisdom here._

---

This document is for any contributors to OpenSlide, including those in
the original OpenSlide group at CMU. It includes some guidelines and
advice.

* Please do not add new API calls without careful thought. Absolutely
  don't add API as unimplemented stubs "just in case". OpenSlide so
  far has been backward compatible in terms of ABI, and part of this
  comes from carefully adding new API only as needed. Removing a bad
  API will come at the cost of binary compatibility.

  I was able to effectively remove the prefetch API without breaking
  ABI by making it a compile time error to link against it, but this
  was only because the API calls were stubs and never implemented and
  never used. Having these unimplemented stubs was a bad idea because
  while the code was unimplemented, no user could possibly test the
  performance implications of using the prefetch; and if we ever
  actually implemented something it would likely hurt performance of
  any user who might have sprinkled prefetch statements around and
  noticed no performance issues with it.

* Make sure things build on Windows, at least with MinGW. Many users
  of OpenSlide are on Windows. Keep in mind the differences between ELF
  and COFF shared libraries, they can get you. This is especially
  important when an OpenSlide API might consume or return a structure
  from a DLL that OpenSlide links to, in general this is unsafe on Windows.

* When making a release, try to carefully follow the libtool
  and automake versioning rules. Also add a changelog entry, update
  the website, and post to the announce mailing list.

* Try to follow the coding style of nearby code.

* Follow the [`GError` rules][gerror-rules] for reporting errors.

* Maintain thread safety. The `openslide_t` struct is mostly immutable,
  except for the cache (which takes locks) and libtiff (which is sort
  of a disaster).

* Avoid the [midlayer mistake](https://lwn.net/Articles/336262/). The grid
  helpers and cache are there for you.

* Have fun! Graphics are a joy.

---


## Release process

We have issue templates for each type of release.  OpenSlide maintainers can
perform a release by filing a new issue named after the new version to be
released, and checking boxes.

- [OpenSlide](https://github.com/openslide/openslide/issues/new?labels=release&template=release.md)
- [OpenSlide Java](https://github.com/openslide/openslide-java/issues/new?labels=release&template=release.md)
- [OpenSlide Python](https://github.com/openslide/openslide-python/issues/new?labels=release&template=release.md)
  - [Updating for a Python major release](https://github.com/openslide/openslide-python/issues/new?labels=release&template=python-bump.md)
- [openslide-winbuild](https://github.com/openslide/openslide-winbuild/issues/new?labels=release&template=release.md)
