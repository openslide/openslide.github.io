---
title: Using premultiplied ARGB pixel data from OpenSlide
---

{% include links.md %}

OpenSlide's C API produces ARGB pixel data formatted with [premultiplied
alpha].  Since the pixels returned by `openslide_read_region()` and
`openslide_read_associated_image()` are often opaque, developers sometimes
conclude that they can convert the ARGB data to opaque RGB by simply
deleting the alpha channel.  However, this can lead to incorrect results:

- Some whole-slide image formats omit portions of an image in which the
  scanner software detected no interesting pixels.  When these regions are
  read through OpenSlide, the library returns transparent pixels.  (This
  commonly occurs with the main images of Leica and MIRAX slides.  It
  currently cannot occur with associated images, but that may change in the
  future.)  Due to premultiplication, these transparent pixels have an an
  ARGB value of `(0, 0, 0, 0)`.  Chopping off the alpha channel will produce
  black pixels, rather than the white pixels which are often desired.  (Some
  formats can request to be composited onto a background color other than
  white; this is exposed via the `openslide.background-color` property.)

- In downsampled levels, the boundaries between present and absent regions
  of a slide often have a partially-transparent, single-pixel-wide border.
  If the alpha channel is dropped, this will render as a visible dark line
  at the edge of some slide regions.

To properly convert the premultiplied ARGB data to opaque RGB, each color
channel must be multiplied by 255 and divided by the alpha value.  This adds
overhead, but an optimization is possible: almost all pixels have alpha
values of 0 or 255, and these values can be special-cased to avoid the
multiplication and division.

Developers of higher-level language bindings should check whether their
language's image abstraction supports premultiplied alpha.  If so, pixel
data from OpenSlide should be loaded into a language-native image object
with premultiplication left intact.  If not, the pixel data must be
unpremultiplied using the procedure described above.  Binding developers
should verify, via profiling, that their unpremultiplication code is
efficient, since it can otherwise be the source of significant overhead.

## Example: Converting OpenSlide ARGB output to RGBX

In this example, the desired output is an array of `uint8_t` with 4 samples
per pixel in R-G-B-X order, where the last sample is a dummy (ignored) alpha
value.  OpenSlide emits samples as `uint32_t`, so on little-endian systems
the output will need to be byte-swapped relative to the input.  For
efficiency in the common case, we treat the output as an array of
`uint32_t`.

```C
#include <glib.h>

uint32_t *buf = g_new(uint32_t, w * h);
uint32_t *out = g_new(uint32_t, w * h);
openslide_read_region(osr, buf, ..., w, h);
for (int64_t i = 0; i < w * h; i++) {
    uint32_t pixel = buf[i];
    uint8_t a = pixel >> 24;
    if (a == 255) {
        // Common case.  Compiles to a shift and a BSWAP.
        out[i] = GUINT32_TO_BE(pixel << 8);
    } else if (a == 0) {
        // Less common case.  Hardcode white pixel; could also
        // use value from openslide.background-color property
        // if it exists
        out[i] = GUINT32_TO_BE(0xffffff00u);
    } else {
        // Unusual case.
        uint8_t r = 255 * ((pixel >> 16) & 0xff) / a;
        uint8_t g = 255 * ((pixel >> 8) & 0xff) / a;
        uint8_t b = 255 * (pixel & 0xff) / a;
        out[i] = GUINT32_TO_BE(r << 24 | g << 16 | b << 8);
    }
}
```

[premultiplied alpha]: http://en.wikipedia.org/wiki/Alpha_compositing#Description
