Starting in OpenSlide 3.4.0, the `OPENSLIDE_DEBUG` environment variable can contain a comma-separated list of debug options that will affect the behavior of the library.  Pass `OPENSLIDE_DEBUG=help` for a list of debug options supported by your copy.

### Options

Option | Description
-------|------------
`detection` | Log the error message returned by each format driver that does *not* detect support for the specified slide file during `openslide_detect_vendor()`, `openslide_can_open()`, or `openslide_open()`.  Useful if `openslide_open()` returns `NULL` when you think it shouldn't.
`jpeg-markers` | For Hamamatsu VMS and NDPI slides, locate all restart markers and perform an extra verification pass before `openslide_open()` returns.  Slow.
`performance` | Log conditions causing OpenSlide to exhibit suboptimal performance.
`tiles` | Draw tile outlines and coordinates in `openslide_read_region()` output.