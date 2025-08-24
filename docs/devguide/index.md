---
title: Developer Guide
---

{% include links.md %}

For now, the main developer documentation is the
[Adding a New Format][doc-newformat] page.  Take particular note of the
section on error handling, but the entire page is worth reading.

The [other developer docs][doc-dev] may also be useful.


## Contributing your code

First, if you are a new contributor to open-source software, please read
[this introduction][rjones] to contributing patches upstream.  Some of the
technical details are obsolete, but the general principles are still valid.

Every contribution to OpenSlide must include a signoff certifying that you
have the right to contribute your changes to the OpenSlide project.  See
[this guide][doc-signoff] for details.

Pull requests that make significant changes should generally be structured
as [multiple commits][rjones-splitting-commits], where each commit is a
self-contained change that evolves the codebase toward the desired outcome.
For example, there might be one commit to fix a typo you found during
development, then a commit that moves some code to a helper function, then a
commit that uses the helper function to add the bare bones of a new feature,
then two more commits that extend that new feature.  Each commit should have
a commit message that describes the reasoning for the change.  When
addressing feedback from code review, edit your existing commits with `git
rebase -i` and update the branch with `git push -f`, rather than appending
fixup commits to the branch.

OpenSlide uses Git hooks and the [pre-commit][pre-commit] framework to
check coding style when you commit.  To configure the hooks, install
pre-commit from your package manager or with `pip install pre-commit`, then
run `pre-commit install` in your OpenSlide checkout.  The pre-commit checks
are also rerun as part of OpenSlide's CI.

Please discuss your changes on the [openslide-users][users-subscribe]
mailing list or in a GitHub issue, *before* you are ready to submit them, so
that we can help you integrate your code into the existing codebase.

When contributing support for a new format, we *strongly* prefer that you
also [contribute example slide files][submit-sample] for our
[openslide-testdata][testdata] repository.  The example files must be data
that you are entitled to contribute, and the OpenSlide project must receive
permission to redistribute them under the [Creative Commons Zero][cc0]
license.  See the [submission form][submit-sample] for more details.

[rjones]: https://people.redhat.com/~rjones/how-to-supply-code-to-open-source-projects/
[rjones-splitting-commits]: https://people.redhat.com/~rjones/how-to-supply-code-to-open-source-projects/#split_patches
[pre-commit]: https://pre-commit.com/
[cc0]: https://creativecommons.org/publicdomain/zero/1.0/legalcode


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
perform a release by filing a new issue and checking boxes.

- [OpenSlide](https://github.com/openslide/openslide/blob/main/.github/maintainer/README.md)
- [OpenSlide Java](https://github.com/openslide/openslide-java/blob/main/.github/maintainer/README.md)
- [OpenSlide Python](https://github.com/openslide/openslide-python/blob/main/.github/maintainer/README.md)
- [openslide-bin](https://github.com/openslide/openslide-bin/blob/main/.github/maintainer/README.md)
