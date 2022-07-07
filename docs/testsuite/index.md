---
title: Using the OpenSlide test suite
---

{% include links.md %}

## Setting up your system

To run the test suite, you will need:

- A Git checkout of OpenSlide
- &ge; 120 GB of disk space (25 GB on XFS, btrfs, or APFS)
- PyYAML
- python-requests
- `xdelta3`
- `cjpeg` and `djpeg`, from libjpeg
- At least one installed font

Valgrind mode requires:

- Valgrind
- Debug symbols for library dependencies (particularly glib2) and Fontconfig

Profile mode requires:

- Valgrind

Coverage mode requires:

- gcov
- Doxygen


## Running test cases

Run all test cases with:

    ./driver run

To run a subset of the test cases, you can use a glob pattern:

    ./driver run 'mirax*'

You can also run the test cases under Valgrind.  This will catch memory
leaks, invalid memory accesses, double frees, etc.  It is also very slow.

    ./driver valgrind

To generate a test coverage report:

    ./driver coverage out.txt

To report `openslide_open()` times for primary test cases:

    ./driver time

### Expected failures

On some platforms, certain test cases may fail due to problems in other
libraries.  To prevent those cases from cluttering the test report, you can
set the `OPENSLIDE_TEST_XFAIL` and/or `OPENSLIDE_VALGRIND_XFAIL` environment
variables to a comma-separated list of cases which are expected to fail
during `run` or `valgrind`, respectively.


## Adding new slides

This should only be necessary when adding new slide formats or variants.

Select the smallest appropriate slide file from openslide-testdata and add
it, and its SHA-256 hash, to `test/cases/slides.yaml`.  Then create a
successful test case including these declarations:

```yaml
# This is the "vanilla" test case for the slide
primary: true
# Check properties
properties:
  openslide.vendor: <vendor>
  # Detect inadvertent changes to the quickhash definition
  openslide.quickhash-1: <value>
```


## Creating new test cases

First, choose a slide and create a skeleton test case for it:

    ./driver create Mirax/CMU-1.zip name-of-test-case
    cd cases/name-of-test-case

Edit the slide file(s):

    hexedit slide/CMU-1/Index.dat

Test that your edits produced the desired results:

    ../../try_open slide/CMU-1.mrxs

Edit the test metadata:

    vi config.yaml

If the slide should open successfully, change `success` to `true`.
Otherwise, set `error` to a regular expression matching the error string
that should be returned by `openslide_get_error()` after `openslide_open()`
returns.

If `openslide_detect_vendor()` should return a different result than for the
original slide (e.g., if OpenSlide falls back to `generic-tiff`), change
`vendor` to the new string or `null` for NULL.

If the test should only be run if particular OpenSlide dependencies are
available, set `requires` to a list of feature flags.  Currently there are
no defined feature flags.

Pack the test:

    cd ../..
    ./driver pack name-of-test-case

This will generate binary diffs of the modified slide file(s).

Finally, commit files to Git:

* `test/cases/name-of-test-case/config.yaml`
* `test/cases/name-of-test-case/*.xdelta`
* `test/cases/name-of-test-case/*.whiteout`

### Annotated `config.yaml`

```yaml
# The openslide-testdata file containing the slide, and the relative path
# within that file (if a Zip).  These are set by "./driver create" and you
# shouldn't need to change them.
base: Hamamatsu-vms/CMU-1.zip
slide: CMU-1-40x - 2010-01-12 13.24.05.vms

# true if openslide_open() and any openslide_read_region() calls should
# succeed, false otherwise.
success: false

# If success is false, a regex for the expected openslide_get_error()
# string.  Should be anchored when possible.  May need to be quoted.
error: ^Tile size not consistent$

# The string that should be returned by openslide_detect_vendor(),
# or null.
vendor: hamamatsu

# True if this is the "vanilla" (unmodified) test case for this slide.
# If true, extended tests will be run, and the case will be evaluated
# during "./driver time".  Defaults to false.
primary: false

# Optional list of features required by this test.  If a specified
# feature is not available, the test will be skipped.
requires: [some-library]

# Optional list of debug options to include in the OPENSLIDE_DEBUG
# environment variable.
debug:
  - jpeg-markers

# Optional list of regions to read.  Arguments are in
# openslide_read_region() order: [x, y, level, w, h].
regions:
  - [0, 0, 1, 100, 100]
  - [1000, 1000, 2, 1, 1]

# Optional map of property values to check against the properties returned
# by OpenSlide.
properties:
  openslide.vendor: hamamatsu

# Generate test case files programmatically at unpack time.  Useful when
# test cases can be deterministically produced by a program but their deltas
# are too large to check in.  Of course this introduces a dependency on the
# specified program.  Use with caution, and only as a last resort.
generate:
  ? "CMU-1-40x - 2010-01-12 13.24.05(1,1).jpg"
  : "jpegtran -restart 256B -outfile %(out)s %(in)s"

# Rename or move test case files during unpack.
rename:
  ? "CMU-1-40x - 2010-01-12 13.24.05(1,1).jpg"
  : "subdir/CMU-1-40x - 2010-01-12 13.24.05(1,1).jpg"
```

### Tips

* Before checking in new tests, make sure the committed files are small.
  CI will prevent you from merging a large test case, because once a large
  file is added to the repository, it cannot be removed.  If xdelta is
  producing large diffs, you may need to generate the test case
  programmatically via the `generate` config option.

* Try to follow the existing naming convention for tests.

* Try to use an anchored regular expression in `error`.  If you must use a
  vague regex, add a comment explaining why.

* If your `error` regex has metacharacters in it, you may need to wrap it in
  single or double quotes.

* If you are creating many test cases, you may find the shell functions in
  `misc/bulk-testcase-helper.sh` useful.
