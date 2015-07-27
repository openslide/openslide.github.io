## Getting OpenSlide for Windows

### Precompiled binaries

Regular releases are available from the [OpenSlide website](http://openslide.org/download/#windows_binaries).  Nightly development builds are [also available](http://openslide.cs.cmu.edu/download/snapshots/windows/?C=M;O=D).

### Building from source

OpenSlide is built for Windows using [MinGW-w64](http://mingw-w64.sourceforge.net/).  The easiest way to build OpenSlide and its dependencies is by using the [openslide-winbuild](https://github.com/openslide/openslide-winbuild) script, which can run on Linux or natively on Windows via [Cygwin](http://www.cygwin.com/).

### Python

OpenSlide Python should work on Windows, but is not included in the OpenSlide binary distributions.

## Using OpenSlide on Windows

### Crashes when linked with MSVC 2010 (VC10) or earlier

With VC10 and earlier, you will see crashes at runtime if you link with `/OPT:REF`, which is the default in release builds.  Link with `/OPT:NOREF` or regenerate the import library using the MSVC toolchain.

### Optional components

If you distribute a program that uses OpenSlide, you may wish to omit these utility programs:

```
openslide-quickhash1sum.exe
openslide-show-properties.exe
openslide-write-png.exe
```

These binaries are only necessary if you use OpenSlide Java:

```
openslide.jar
openslide-jni.dll
```

Files with names ending in `.debug` contain debug symbols for GDB, and can also be omitted.

### Licensing

If you distribute OpenSlide binaries, you are also required to distribute the corresponding source code for OpenSlide and some of its dependencies.  The exact license terms for each component are included in the `licenses` directory of OpenSlide binary distributions.  Complete corresponding sources for official builds and nightlies are distributed in the `-winbuild` Zip file alongside the binary Zips.