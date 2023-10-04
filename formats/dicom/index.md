---
title: DICOM format
---

Format
: international standard multi-file medical imaging format

File extensions
: `.dcm`

OpenSlide vendor backend
: `dicom`


## Format Documentation

[DICOM Whole Slide Imaging](https://dicom.nema.org/dicom/dicomwsi/)


## Detection

OpenSlide will detect a file as DICOM if:

 1. The file can be parsed as a DICOM Part 10 file.
 2. The _Media Storage SOP Class UID_ is _VL Whole Slide Microscopy Image
    Storage_ (`1.2.840.10008.5.1.4.1.1.77.1.6`).


## File Organization

OpenSlide uses [libdicom](https://github.com/ImagingDataCommons/libdicom/)
to parse and load DICOM files.

OpenSlide non-recursively scans the containing directory for other DICOM
files with the same _Series Instance UID_ attribute value as the specified
file.  It uses the _Image Type_ attribute of each matching file to determine
the file's role within the whole slide image:

| Role | Allowed _Image Type_ values |
| - | - | - |
| Slide level | `ORIGINAL\PRIMARY\VOLUME\NONE`<br>`DERIVED\PRIMARY\VOLUME\NONE`<br>`DERIVED\PRIMARY\VOLUME\RESAMPLED` |
| Associated image | `ORIGINAL\PRIMARY\LABEL\NONE`<br>`ORIGINAL\PRIMARY\OVERVIEW\NONE`<br>`ORIGINAL\PRIMARY\THUMBNAIL\RESAMPLED`<br>`DERIVED\PRIMARY\LABEL\NONE`<br>`DERIVED\PRIMARY\OVERVIEW\NONE`<br>`DERIVED\PRIMARY\THUMBNAIL\RESAMPLED` |
| Ignored | All others |

If multiple files in the directory have the same _SOP Instance UID_,
the extra copies are ignored.

A file's _Dimension Organization Type_ can be `TILED_FULL`, `TILED_SPARSE`,
or `3D`.  These transfer syntaxes and photometric interpretations are
supported:

| Pixel encoding | _Transfer Syntax UID_ | Allowed _Photometric Interpretation_ values |
| - | - | - |
| Uncompressed little-endian | `1.2.840.10008.1.2.1` | `RGB` |
| JPEG baseline | `1.2.840.10008.1.2.4.50` | `RGB`<br>`YBR_FULL_422` |
| JPEG 2000 | `1.2.840.10008.1.2.4.91` | `RGB`<br>`YBR_ICT` |
| JPEG 2000 lossless | `1.2.840.10008.1.2.4.90` | `RGB`<br>`YBR_ICT` |


## ICC Profiles

The slide ICC profile is taken from the _ICC Profile_ attribute of the
highest-resolution image.  Associated image ICC profiles are taken from the
_ICC Profile_ of the associated image.


## Associated Images

| Associated image | Allowed _Image Type_ values |
| - | - | - |
| thumbnail | `ORIGINAL\PRIMARY\THUMBNAIL\RESAMPLED`<br>`DERIVED\PRIMARY\THUMBNAIL\RESAMPLED` |
| label | `ORIGINAL\PRIMARY\LABEL\NONE`<br>`DERIVED\PRIMARY\LABEL\NONE` |
| macro | `ORIGINAL\PRIMARY\OVERVIEW\NONE`<br>`DERIVED\PRIMARY\OVERVIEW\NONE` |


## Known Properties

Many DICOM attributes are represented hierarchically as properties prefixed
with "`dicom.`".

`openslide.mpp-x`
: normalized X component of _Pixel Spacing_ from highest-resolution level

`openslide.mpp-y`
: normalized Y component of _Pixel Spacing_ from highest-resolution level

`openslide.objective-power`
: _Objective Lens Power_ from highest-resolution level


## Test Data

<https://openslide.cs.cmu.edu/download/openslide-testdata/DICOM/>
