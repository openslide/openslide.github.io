Starting in OpenSlide 3.4.0, the `OPENSLIDE_DEBUG` environment variable can contain a comma-separated list of debug options that will affect the behavior of the library.  Pass `OPENSLIDE_DEBUG=help` for a list of debug options supported by your copy.

### Options

* **jpeg-markers**: For Hamamatsu VMS and NDPI slides, locate all restart markers and perform an extra verification pass before `openslide_open()` returns.  Slow.
* **tiles**: Draw tile outlines and coordinates in `openslide_read_region()` output.
* **unsupported**: During `openslide_open()`, log the error message returned by each format driver that refuses to read the slide file.  Useful if `openslide_open()` returns `NULL` when you think it shouldn't.