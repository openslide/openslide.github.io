---
layout: default
title: Sakura format
---

{% include links.markdown %}

Format
:SQLite database containing pyramid tiles and metadata

File extensions
:`.svslide`

OpenSlide vendor backend
:`sakura`


Detection
---------

OpenSlide will detect a file as Sakura if:

 1. The file is a SQLite database.
 2. The `DataManagerSQLiteConfigXPO` table contains exactly one row, and its `TableName` field refers to a unique table.
 3. The unique table contains a row with `id = "++MagicBytes"` and `data = "SVGigaPixelImage"`.


File Organization
-----------------

Sakura slides are SQLite 3 database files written by the eXpress Persistent
Objects ORM.  Tables contain slide metadata, associated images, and JPEG
tiles.  Tiles are addressed as `(downsample, level-0 X coordinate, level-0 Y
coordinate, color channel)`, with separate grayscale JPEGs for each color
channel.  Despite the generality of the address format, tiles appear to be
organized in a regular grid, with power-of-two level downsamples and without
overlapping tiles.  The structure of the file allows scans to be sparse, but
it is not clear if this is actually done.

SQL Tables
----------

Some irrelevant tables and columns have been omitted from the summary below.

#### `DataManagerSQLiteConfigXPO`

Useful only to get a reference to the unique table.  OpenSlide requires this
table to contain exactly one row.

Column | Type | Description |
-------|------|-------------|
`TableName`|text|Name of the unique table, described below|

#### `SVSlideDataXPO`

High-level metadata about a slide.  OpenSlide assumes this table will
contain exactly one row.

Column | Type | Description |
-------|------|-------------|
`OID`|integer|Primary key|
`m_labelScan`|integer|Foreign key to `label` associated image in `SVScannedImageDataXPO`|
`m_overviewScan`|integer|Foreign key to `macro` associated image in `SVScannedImageDataXPO`|
`SlideId`|text|UUID|
`Date`|text|File creation date?|
`Description`|text|Descriptive text?|
`Creator`|text|Author?|
`DiagnosisCode`|text|Unknown, have seen "0"|
`HRScanCount`|integer|Presumably the number of corresponding rows in `SVHRScanDataXPO`|
`Keywords`|text|Descriptive text?|
`TotalDataSizeBytes`|integer|Presumably the sum of `TotalDataSizeBytes` in corresponding `SVHRScanDataXPO` rows|

#### `SVHRScanDataXPO`

A single high-resolution scan of a slide from `SVSlideDataXPO`.  OpenSlide
assumes this table will contain exactly one row.

Column | Type | Description |
-------|------|-------------|
`OID`|integer|Primary key|
`ParentSlide`|integer|Foreign key to `SVSlideDataXPO`|
`ScanId`|text|UUID|
`Date`|text|Scan date?|
`Description`|text|Descriptive text?|
`Name`|text|Scan name?|
`PosOnSlideMm`|blob|16 bytes of binary|
`ResolutionMmPerPix`|real|Millimeters per pixel|
`NominalLensMagnification`|real|Objective power|
`ThumbnailImage`|blob|`thumbnail` associated image data|
`TotalDataSizeBytes`|integer|Same as `TOTAL_SIZE` blob in unique table|
`FocussingMethod`|integer|Unknown; have seen "1"|
`FocusStack`|blob|8 bytes; have seen all zeros|

#### `SVScannedImageDataXPO`

Contains associated images other than the `thumbnail`.

Column | Type | Description |
-------|------|-------------|
`OID`|integer|Primary key|
`Id`|text|UUID|
`PosOnSlideMm`|blob|16 bytes of binary|
`ScanCenterPosMm`|blob|16 bytes of binary|
`ResolutionMmPerPix`|real|Millimeters per pixel|
`Image`|blob|JPEG image data|
`ThumbnailImage`|blob|Low-resolution JPEG thumbnail|

#### `tile`

This table is most naturally used to map tile coordinates to tile IDs, but
is not suitable for individual lookups because it has no useful indexes.

Column | Type | Description |
-------|------|-------------|
`TILEID`|text|Foreign key to unique table|
`PYRAMIDLEVEL`|integer|Downsample of the pyramid level|
`COLUMNINDEX`|integer|Level-0 X coordinate of the top-left corner of the tile|
`ROWINDEX`|integer|Level-0 Y coordinate of the top-left corner of the tile|
`COLORINDEX`|integer|0 for red, 1 for green, 2 for blue|

#### Unique table

This is the table named by `DataManagerSQLiteConfigXPO.TableName`.  It
contains named blobs including the JPEG tile data.

Column | Type | Description |
-------|------|-------------|
`id`|text|Primary key|
`size`|integer|Length of `data` field|
`data`|blob|Data item|

This table stores a variety of blob types.  IDs for image tiles appear to be
mechanically generated from the tile coordinates, but OpenSlide does not
construct them directly.  Instead, it uses the `tile` table to obtain IDs
for each tile.

`id` | Description |
-----|-------------|
`++MagicBytes`|`SVGigaPixelImage`|
`++VersionBytes`|Format version, e.g. `1.0.0`|
`Header`|A small binary structure.  The first 12 bytes are little-endian 32-bit integers: tile size in pixels, image width in pixels, image height in pixels.|
`TOTAL_SIZE`|The `data` field is empty.  The `size` field is the sum of all other `size` fields except `++MagicBytes` and `++VersionBytes`.|
T;2048&#124;4096;4;2;0|Image tile with downsample 4, X coordinate 2048, Y coordinate 4096, channel 2 (blue)|
T;2048&#124;4096;4;2;0#|MD5 hash of the T;2048&#124;4096;4;2;0 image tile|


Associated Images
-----------------

`label`
:`SVScannedImageDataXPO.Image` corresponding to `SVSlideDataXPO.m_labelScan`

`macro`
:`SVScannedImageDataXPO.Image` corresponding to `SVSlideDataXPO.m_overviewScan`

`thumbnail`
:`SVHRScanDataXPO.ThumbnailImage`


Known Properties
----------------

`sakura.Creator`
:`SVSlideDataXPO.Creator`

`sakura.Date`
:`SVSlideDataXPO.Date`

`sakura.Description`
:`SVSlideDataXPO.Description`

`sakura.DiagnosisCode`
:`SVSlideDataXPO.DiagnosisCode`

`sakura.FocussingMethod`
:`SVHRScanDataXPO.FocussingMethod`

`sakura.Keywords`
:`SVSlideDataXPO.Keywords`

`sakura.NominalLensMagnification`
:`SVHRScanDataXPO.NominalLensMagnification`

`sakura.ResolutionMmPerPix`
:`SVHRScanDataXPO.ResolutionMmPerPix`

`sakura.ScanId`
:`SVHRScanDataXPO.ScanId`

`sakura.SlideId`
:`SVSlideDataXPO.SlideId`

`openslide.mpp-x`
:calculated as `1000 * sakura.ResolutionMmPerPix`

`openslide.mpp-y`
:calculated as `1000 * sakura.ResolutionMmPerPix`

`openslide.objective-power`
:normalized `sakura.NominalLensMagnification`


Test Data
---------

No public data available.  Contact the [mailing list][users-subscribe] if
you have some.
