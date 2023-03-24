<!--
 ~ Copyright DB Netz AG and contributors
 ~ SPDX-License-Identifier: Apache-2.0
 -->

[[_TOC_]]

## 1.0.0
Release

### 1.1.0
- Added raillabel.filter() and raillabel.Scene.filter()
- Fixed a bug when comparing raillabel.CoordinateSystems with differing base children

#### 1.1.1
- Fixed a naming dispute in raillabel.save()
- Tested the package for Python 3.8 and 3.10
- Created a requirements.txt
- The filter() function is now accessible via raillabel.filter() instead of raillabel.io.filter()

### 1.2.0
- Implemented frame specific data, that does not belong to any object
- Implemented the Num annotation type

## 2.0.0
- Made the saved data VCD-compatible
  - URIs of the annotation files (like the .png, where a bounding box is located) are now stored in the "frame_properties" under "sensors"
  - Implemented object data pointers
  - Devkit version is now stored in the metadata
- FrameInterval.\_\_len\_\_() now returns the number of frames in the FrameInterval
- Frame.annotations returns a dict of all annotations in the frame regardless of type or object
- Removed proprietary parts
- Added poly3d as a supported annotation type
- All annotations are now stored in object_data.annotations (before they were stored in different fields according to their type)
- raillabel.Scene.filter() has been removed. Use raillabel.filter() instead
- Fields "coordinate_system" and "frame_intervals" have been removed from the raillabel.format.Object class
- stream and coordinate system have been combined into a single sensor type

## 2.0.1
- Changed name of PyPI package from 'raillabel' to 'pyraillabel' due to name collision

## 2.0.2
- Changed name of PyPI package back to 'raillabel' because the problematic package has been removed

## 2.0.3
- Fixed bug related to saving the annotator field in the metadata
