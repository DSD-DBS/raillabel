<!--
 ~ Copyright DB InfraGO AG and contributors
 ~ SPDX-License-Identifier: Apache-2.0
 -->

# 1.0.0
Release

## 1.1.0
- Added raillabel.filter() and raillabel.Scene.filter()
- Fixed a bug when comparing raillabel.CoordinateSystems with differing base children

### 1.1.1
- Fixed a naming dispute in raillabel.save()
- Tested the package for Python 3.8 and 3.10
- Created a requirements.txt
- The filter() function is now accessible via raillabel.filter() instead of raillabel.io.filter()

## 1.2.0
- Implemented frame specific data, that does not belong to any object
- Implemented the Num annotation type

# 2.0.0
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

### 2.0.1
- Changed name of PyPI package from 'raillabel' to 'pyraillabel' due to name collision

### 2.0.2
- Changed name of PyPI package back to 'raillabel' because the problematic package has been removed

### 2.0.3
- Fixed bug related to saving the annotator field in the metadata

### 2.0.4
- Fixed bug related to the package version

## 2.1.0
- Added IntrinsicsRadar to the devkit and the json-schema

## 2.2.0
- Raillabel schema is now more restrictive regarding intrinsic calibration
- Support for understand.ai t4 format
- Renaming of raillabel.format.Frame.data to frame_data

### 2.2.1
- Fixed bug, that prevented loading a understand ai file via raillabel.load()
- Made the project_id field in the understand ai files less restrictive

## 2.3.0
- Support for additional, undefined attributes in raillabel.format.Metadata

# 3.0.0
- Removed deprecated features
- Annotation classes now contain information about the object they annotate
- Removed ```ObjectData``` - frames now directly contain the annotations
- ```name``` field in annotation classes now is automatically generated
- Separated ```frame_data``` and ```object_data``` in the schema and devkit
  - ```frame_data``` can only contain ```Num``` instances
  - ```object_data``` can not contain ```Num``` instances anymore
- Major restructuring of the project directories
- ```FrameInterval.from_frame_ids()```: create ```FrameIntervals``` by providing a list of frame uids
- ```Object.object_data_pointers()```: generate ```ElementDataPointers```
- ```Scene.frame_intervals()```, ```Object.frame_intervals()```: generate ```FrameIntervals```
- ```Object.asdict()``` now provides also frame intervals and object data pointers, if the frames from the scene are provided
- ```Scene.fromdict()``` for loading a scene from a dictionary

### 3.0.1
- ```LoaderUnderstandAi``` now passes the warnings from the ```LoaderRaillabel``` onto the user
- ```LoaderUnderstandAi.load()``` ```validate``` parameter defaults to ```False``` now

## 3.1.0
- ```LoaderUnderstandAi``` now includes warnings for duplicate annotation id and duplicate frame id
- ```LoaderRaillabel``` now includes a warniing for duplicate frame id

## 3.2.0
- Introduce support for Python 3.12

### 3.2.1
- Fix bug related to Python 3.12

## 3.3.0
- Introduce support for Python 3.13

### 3.3.1
- Add DeprecationWarnings for all functionalities, that have changed in 4.0.0

# 4.0.0
New Major changes to RailLabel! Over the time two major use cases for this package have crystalized. The first one are the users of the data sets published by Deutsche Bahn. The second one are the contractors providing the annotations. Since the two groups have vastly different requirements for this package, we decided to split it accordingly.

If you just want to work with out data, then you are in luck. You can just continue using this package with even more focus on your needs.

If you are building raillabel scenes yourself or want to manipulate the data in a safe way, then the [raillabel_providerkit](https://github.com/DSD-DBS/raillabel-providerkit) is for you. All functionality you may be missing in this new raillabel version will be provided over there with even better APIs.

Functionality, that has been **moved** to the `raillabel_providerkit`:
- loading annotations in formats other than raillabel itself
- validating the content of files

Other breaking changes:
- the `fromdict()` and `asdict()` methods in `raillabel.format` classes have been replaced with `from_json()` and `to_json` respectively
- `raillabel.format.FrameInterval` fields have been changed by `frame_start -> start` and `frame_end -> end` to make it more concise
- all uid fields of classes have been removed (like `raillabel.format.Frame.uid`) have been removed to avoid redundant information
- `raillabel.format.Sensor` has been removed in favor of the different sensor type classes `raillabel.format.Camera`, `raillabel.format.Lidar`, `raillabel.format.Radar` and `raillabel.format.GpsImu`
- `raillabel.filter()` has been removed in favor of `raillabel.Scene.filter()` with different input arguments

New features:
- `raillabel.json_format` has been introduced as an interface between the JSON format and the `raillabel` classes
- `raillabel.scene_builder.SceneBuilder` is now available to easily build scenes for testing purposes

# 4.1.0
- Add value arguments to `SceneBuilder.add_bbox()`, `SceneBuilder.add_cuboid()`, `SceneBuilder.add_poly2s()`, `SceneBuilder.add_poly3d()` and `SceneBuilder.add_seg3d()` like `SceneBuilder.add_bbox(pos=Point2d(1.0, 2.0))`

# 4.1.1
- `Scene.filter()` now also removes unused sensors from `Frame.sensors`
- `SceneBuilder` now also automatically adds sensors to `Frame.sensor` if a frame has a timestamp value
