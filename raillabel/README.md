
<!--
 ~ Copyright DB Netz AG and contributors
 ~ SPDX-License-Identifier: Apache-2.0
 -->

# RailLabel
A devkit for working with recorded and annotated train ride data from Deutsche Bahn.

## Overview
[[_TOC_]]

## Motivation and OpenLABEL
Working with our own data has brought up the need to interact with the annotations programmatically. The annotation data is stored in .json files in the [ASAM OpenLABEL](https://www.asam.net/standards/detail/openlabel/) annotation format, an emerging industry standard targeted towards the automotive sector. But as a standard it is designed very inclusively, which makes it overloaded for our limited use cases. Therefore, we decided to create a data model with Python dataclasses, that makes it easier to interact with our data than just loading the JSON and handling it like a dictionary. The example below shows a comparison between the two approaches.

With JSON only:
``` Python
import json

with open('path/to/file.json', 'w') as data_file:
    scene = json.load(data_file)

    scene['openlabel']['frames']['0']['frame_properties']['streams']['lidar']['stream_properties']['stream_sync']['timestamp'] += 37

    json.dump(scene)
```

With RailLabel
``` Python
import raillabel

scene = raillabel.load('path/to/file.json')
scene.frames['0'].stream_stamps['lidar'].timestamp += 37
raillabel.save(scene, 'path/to/file.json')
```

Furthermore, this enables the use of data integrity checks built into the functions.

## Deviation from the OpenLABEL Standard
As OpenLABEL has not been specifically developed for the railway use case, it does not cover 100% of our annotation needs. We therefore adapted some OpenLABEL features to cover the rest of these needs.

- `$.openlabel.metadata.tagged_file` stores the folder name for the exported scene data
- The vec data type stores point cloud segmentation data (each element represents the index of a point in the point cloud file)
- Each annotation has an attribute called 'uri', which contains the name of the file this annotation is referenced in (i.e. the name of the image file a bounding box should be drawn in)
- The uri-property of each stream contains its rostopic

# Getting Started

## Requirements
RailLabel requires the following to run:
```
python>=3.8.13
jsonschema>=4.4.0
scipy>=1.7.0
```

## Installation
```
git clone git@ssh.dev.azure.com:v3/DB-Netz/DAE/raillabel-devkit
```

# Usage
The base class for the annotations is a raillabel.format.Scene. This class contains all information of exactly one annotation file and is the interface for the functions listed below

## RailLabel Functions

### validate()
This function validates JSON data represented by a dict via a given schema and returns the validation status as well as any found errors. This function does not need to be called before calling [load()](#load) or [save()](#save), since they do it automatically.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
|data|False| dict | JSON data to be validated|
|schema_path | True | str | Path to the JSON schema used for the validation. If the schema is in the /io/schemas folder, the format name can be used (i.e. schema_path can be 'openlabel_v1' or 'openlabel_v1_schema' to load the openlabel_v1_schema.json file). Default is 'openlabel_v1'.|

**Return Value:**
validate() returns 2 values in a tuple, one is the boolean validation status with True meaning that the data validates against the JSON schema. The second parameter is a list of warning messages, that tell the user, where the errors in the JSON data are. This is only relevant, if the first return value is False, though.

**Example:**
``` Python
is_data_valid, warnings = raillabel.validate(data)

if is_data_valid:
    do_something()

else:
    for w in warnings:
        print(w)
```

### load()
This function loads an annotation file by identifying and calling a suitable loader class and returns the data as a raillabel.Scene. load() can also be used not only for data in the OpenLABEL format, but also in other supported formats.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| path | False | str | Path to the annotation file. |
| validate | True | bool | If True, the annotation data is validated via the OpenLabel schema. This is highly recommended, as not validating the data may lead to Errors during loading or while handling the scene.  However, validating may increase the loading time. Default is True.|

**Example:**
``` Python
import raillabel
scene = raillabel.load('path/to/file.json')
```

### save()
This function stores a raillabel.Scene in a JSON file. The JSON is in the ASAM OpenLabel annotation format and is validated via the OpenLabel schema.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| scene | False | [raillabel.Scene](#scene) | Scene, which should be saved. |
| save_path | False | str | Path to the JSON file. |
| quiet | True | bool | If true, only minimal console output is produced. Default is True. |
| prettify_json | True | bool | If true, the JSON is saved with linebreaks and indents. This increases readibility but also the file size. Default is False. |

**Example:**
``` Python
import raillabel

scene = raillabel.load('path/to/file.json')
scene.frames['0'].stream_stamps['lidar'].timestamp += 37
raillabel.save(scene, 'path/to/file.json')
```

### filter()
This function returns a copy of the inserted scene containing only the annotations that the given filter parameters apply to.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| scene | False | [raillabel.Scene](#scene) | Scene, which should be copied and filtered. |
| include_classes | True | str or list of str | List of class/type names that should be included in the filtered scene. If set, no other classes/types will be copied. Mutually exclusive with exclude_classes. |
| exclude_classes | True | str or list of str | List of class/type names that should be excluded in the filtered scene. If set, all other classes/types will be copied. Mutually exclusive with include_classes. |
| include_annotation_types | True | str or list of str | List of annotation types (i.e. bboxs, cuboids, poly2ds, seg3ds) that should be included in the filtered scene. If set, no other annotation types will be copied. Mutually exclusive with exclude_annotation_types. |
| exclude_annotation_types | True | str or list of str | List of annotation types (i.e. bboxs, cuboids, poly2ds, seg3ds) that should be excluded in the filtered scene. If set, all other annotation types will be copied. Mutually exclusive with include_annotation_types. |
| include_annotation_ids | True | str or list of str | List of annotation UIDs that should be included in the filtered scene. If set, no other annotation UIDs will be copied. Mutually exclusive with exclude_annotation_ids. |
| exclude_annotation_ids | True | str or list of str | List of annotation UIDs that should be excluded in the filtered scene. If set, all other annotation UIDs will be copied. Mutually exclusive with include_annotation_ids. |
| include_object_ids | True | str or list of str | List of object UIDs that should be included in the filtered scene. If set, no other objects will be copied. Mutually exclusive with exclude_object_ids. |
| exclude_object_ids | True | str or list of str | List of object UIDs that should be excluded in the filtered scene. If set, all other objects will be copied. Mutually exclusive with include_object_ids. |
| include_sensors | True | str or list of str | List of sensors that should be included in the filtered scene. If set, no other sensors will be copied. Mutually exclusive with exclude_sensors. |
| exclude_sensors | True | str or list of str | List of sensors that should be excluded in the filtered scene. If set, all other sensors will be copied. Mutually exclusive with include_sensors. |
| include_attributes | True | dict | Dict of attributes that should be included in the filtered scene. Dict keys are the attribute names, values are the specific values that should be included. If the value is set so None, all annotations with the attribute are included regardless of value. Mutually exclusive with exclude_attributes. |
| exclude_attributes | True | dict | Dict of attributes that should be excluded in the filtered scene. Dict keys are the attribute names, values are the specific values that should be excluded. If the value is set so None, all annotations with the attribute are excluded regardless of value. Mutually exclusive with include_attributes. |
| include_frames | True | int or list of int | List of frame UIDs that should be included in the filtered scene. If set, no other frames will be copied. Mutually exclusive with exclude_frames. |
| exclude_frames | True | int or list of int | List of frame UIDs that should be excluded in the filtered scene. If set, all other frames will be copied. Mutually exclusive with include_frames. |
| start_frame | True | int | Frame at which the filtered scene should start. Mutually exclusive with start_timestamp. |
| end_frame | True | int | Frame at which the filtered scene should end (inclusive). Mutually exclusive with end_timestamp. |
| start_timestamp | True | [decimal.Decimal](https://docs.python.org/3/library/decimal.html#decimal.Decimal) | Unix timestamp at which the filtered scene should start (inclusive). Mutually exclusive with start_frame. |
| end_timestamp | True | [decimal.Decimal](https://docs.python.org/3/library/decimal.html#decimal.Decimal) | Unix timestamp at which the filtered scene should end (inclusive). Mutually exclusive with end_frame. |

**Returns:**

Scene with the filters applied.

**Example:**
``` Python
import raillabel
import decimal

scene = raillabel.load('path/to/file.json')

scene_with_only_trains = raillabel.filter(
    scene,
    include_classes='train'
)
scene_without_bboxs = raillabel.filter(
    scene,
    exclude_annotation_types=['bbox']
)
cut_scene_with_only_red_trains = raillabel.filter(
    scene,
    start_timestamp=decimal.Decimal('1587349200.004200000'),
    exclude_frames=[4, 2],
    include_classes='train',
    include_attributes={
        'color': 'red'
    }
)
scene_with_annotations_with_an_attribute = raillabel.filter(
    scene,
    include_attributes={ # All annotations with the color
        'color': None    # attribute will be included,
    }                    # regardless of color value.
)

invalid_scene = raillabel.filter(
    scene,
    include_classes='person',  # Will raise a ValueError due
    exclude_classes='train'    # to mutual exclusivity.
)
```

## RailLabel Format Dataclasses
The dataclasses form the framework, which allows easy access to the data. Most data classes contain a function called asdict(), which returns a dictionary with the data formated according to the OpenLABEL schema.

### **Scene**
The root RailLabel class, which contains all annotations. Can be accessed via raillabel.Scene or raillabel.format.Scene.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| metadata | False | [raillabel.format.Metadata](#metadata) | This object contains information, that is, metadata, about the annotation file itself. |
| streams | True | dict of [raillabel.format.Stream](#stream) | Dictionary of raillabel.format.Streams. Dictionary keys are the stream uids. Default is {}. |
| coordinate_systems | True | dict of [raillabel.format.CoordinateSystem](#coordinatesystem) | Dictionary of raillabel.format.CoordinateSystems. Dictionary keys are strings. Default is {}. |
| objects | True | dict of [raillabel.format.Object](#object) | Dictionary of raillabel.format.Objects. Dictionary keys are uuid.UUIDs. Default is {}. |
| frames | True | dict of [raillabel.format.Frame](#frame) | Dict of frames in the scene. Dictionary keys are the frame uids. Default is {}. |

**Methods:**

filter(): see [raillabel.filter()](#filter).

**Example:**
``` Python
import raillabel

scene = raillabel.Scene(
    metadata=raillabel.format.Metadata(
        schema_version='1.0.0'
    )
)
scene_with_only_trains = scene.filter(
    include_classes='train'
)
```

### **Metadata**
This class contains information, that is, metadata, about the annotation file itself.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| schema_version | False | str | Version number of the RailLabel schema this annotation object follows. |
| annotator | True | str | Name or description of the annotator that created the annotations. Default is None. |
| comment | True | str | Additional information or description about the annotation content. Default is None. |
| file_version | True | str | Version number of the RailLabel annotation content. Default is None. |
| name | True | str | Name of the RailLabel annotation content. Default is None. |
| tagged_file | True | str | Directory with the exported data (e.g. images, point clouds). Default is None. |

**Example:**
``` Python
import raillabel

metadata = raillabel.format.Metadata(
    schema_version='1.0.0',
    comment='This is an example',
    name='project_foo',
    file_version='1.0.0',
    tagged_file='/project_foo/data'
)
```

### **Stream**
A stream describes the source of a data sequence, usually a sensor.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| uid | False | str | Unique identifier of the stream. Commonly a friendly name. |
| type | False | str | A string encoding the type of the stream. The only valid values are 'camera', 'lidar', 'radar', 'gps_imu' or 'other'. |
| calibration | True | [raillabel.format.StreamCalibration](#streamcalibration) | Intrinsic calibration of the stream. Default is None. |
| rostopic | True | str | The name of the rostopic of the stream. Default is None. |
| description | True | str | Description of the stream. Default is None. |

**Example:**
``` Python
import raillabel

stream = raillabel.format.Stream(
    uid='rgb_left',
    type='camera',
    rostopic='/rgb_left/image',
    description='Just some RGB camera on the left.'
)
```

### **StreamCalibration**
Intrinsic calibration for a camera stream.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| camera_matrix | False | tuple of float of length 12 | This is a 3x4 camera matrix which projects 3D homogeneous points (4x1) from a camera coordinate system into the image plane (3x1). This is the usual K matrix for camera projection as in OpenCV. It is extended from 3x3 to 3x4 to enable its direct utilisation to project 4x1 homogeneous 3D points. The matrix is defined to follow the camera model: x-to-right, y-down, z-forward. The following equation applies: x_img = camera_matrix * X_ccs. |
| distortion | False | tuple of float of length 5 to 14 | This is the array 1xN radial and tangential distortion coefficients. |
| width_px | True | int | Width of the image frame in pixels. Default is None. |
| height_px | True | int | Height of the image frame in pixels. Default is None. |

**Example:**
``` Python
import raillabel

stream_cal = raillabel.format.StreamCalibration(
    camera_matrix=(
        0.48, 0,    0.81, 0,
        0,    0.16, 0.83, 0,
        0,    0,    1,    0
    ),
    distortion=(
        0.49,
        0.69,
        0.31,
        0.81,
        0.99
    ),
    width_px=2464,
    height_px=1600
)
```

### **CoordinateSystem**
A coordinate system is a 3D reference frame. Spatial information on objects and their properties can be defined with respect to coordinate systems.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| uid | False | str | This is the friendly name of the coordinate_system as well as its identifier. Must be unique. |
| type | False | str | This is a string that describes the type of the coordinate system, for example, "local", "sensor", "geo". |
| parent | True | [raillabel.format.CoordinateSystem](#coordinatesystem) | A reference to the parent coordinate system, this CoordinateSystem is based on. If this this coordinate system has no parent (i.e. the base coordinate system), the parent should be None. Default is None. |
| children | True | dict of [raillabel.format.CoordinateSystem](#coordinatesystem) | Dictionary of children of this coordinate system. Dict keys are the uid strings of the child coordinate system. Dict values are references to those children. Default is {}. |
| transform | True | [raillabel.format.Transform](#transform) | A transformation between this coordinate systems and its parent. Default is None. |

**Example:**
``` Python
import raillabel

base_cs = raillabel.format.CoordinateSystem(
    uid='base',
    type='local',
    parent=None,
    children=[]
),

rgb_left_cs = raillabel.format.CoordinateSystem(
    uid='rgb_left',
    type='sensor',
    parent=base_cs,
    children=[],
    transform=raillabel.format.Transform(
        pos=raillabel.format.Point3d(
            x=0,
            y=1,
            z=2
        ),
        quat=raillabel.format.Quaternion(
            x=0.97518507,
            y=-0.18529384,
            z=-0.05469746,
            w=-0.10811315
        )
    )
)

base_cs.children.append(rgb_left_cs)
```

### **Transform**
A transformation between two coordinate systems.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| pos | False | [raillabel.format.Point3d](#point3d) | Translation with regards to the parent coordinate system. |
| quat | False | [raillabel.format.Quaternion](#quaternion) | Rotation quaternion with regards to the parent coordinate system. |

**Example:**
``` Python
import raillabel

transform = raillabel.format.Transform(
    pos=raillabel.format.Point3d(
        x=0,
        y=1,
        z=2
    ),
    quat=raillabel.format.Quaternion(
        x=0.97518507,
        y=-0.18529384,
        z=-0.05469746,
        w=-0.10811315
    )
)
```

### **Object**
An object is the main type of annotation element. Object is designed to represent spatiotemporal entities, such as physical objects in the real world. Objects shall have a name and type. Objects may have static and dynamic data. Objects are the only type of elements that may have geometric data, such as bounding boxes, cuboids, polylines, images, etc. Objects are connected with these annotations via the ObjectAnnotation class instances.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| uid | False | str | This a string representing the unique universal identifier for the object. |
| name | False | str | Name of the object. It is a friendly name and not used for indexing. Commonly the class name is used followed by an underscore and an integer (i.e. person_0032). |
| type | False | str | The type of an object defines the class the object corresponds to. |
| coordinate_system | True | [raillabel.format.CoordinateSystem](#coordinatesystem) | This is the coordinate system this object is referenced in. Default is None. |
| frame_intervals | True | list of [raillabel.format.FrameInterval](#frameinterval) | The array of frame intervals where this action exists or is defined. Default is []. |

**Example:**
``` Python
import raillabel

obj = raillabel.format.Object(
    uid='6fe55546-0dd7-4e40-b6b4-bb7ea3445772',
    name='person_0000',
    type='person',
    frame_intervals=[
        raillabel.format.FrameInterval(
            frame_start=0,
            frame_end=5
        ),
        raillabel.format.FrameInterval(
            frame_start=12,
            frame_end=14
        )
    ]
)
```

### **FrameInterval**
A frame interval defines a starting and ending frame number as a closed interval. That means the interval includes the limit frame numbers.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| frame_start | False | int | Initial frame number of the interval. |
| frame_end | False | int | Ending frame number of the interval. |

**Example:**
``` Python
import raillabel

interval = raillabel.format.FrameInterval(0, 5)
```

### **Frame**
A frame is a container of dynamic, timewise, information.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| uid | False | int | Number of the frame withing the annotation file. Must be unique. |
| timestamp | False | [decimal.Decimal](https://docs.python.org/3/library/decimal.html#decimal.Decimal) | Timestamp containing the Unix epoch time of the frame with up to nanosecond precision. |
| stream_stamps | True | dict of [raillabel.format.StreamStamp](#streamstamp) | Timestamps dictionary containing the StreamStamp objects. Dictionary keys are the stream uids. Default is {}. |
| data | True | dict | Dict containing the data concerning this frame and not any object (e.g. vehicle speed, position). Default is {}. |
| objects | True | dict of [raillabel.format.ObjectAnnotations](#objectannotations) | Dictionary containing the annotations per object. Dictionary keys are the object uids. Default is {}. |

**Read-Only Properties:**
| Name | Type | Description |
| annotations | dict | Dictionary containing all annotations of this frame, regardless of object or annotation type. Dictionary keys are annotation UIDs. |

**Example:**
``` Python
import raillabel
from decimal import Decimal

frame = raillabel.format.Frame(
    uid=1,
    timestamp=Decimal('1632321743.134149000'),
    stream_stamps={
        'rgb_left': raillabel.format.StreamStamp(
            stream=raillabel.format.Stream(
                uid='rgb_left',
                type='camera'
            ),
            timestamp=Decimal('1632321743.100000072')
        ),
        'lidar': raillabel.format.StreamStamp(
            stream=raillabel.format.Stream(
                uid='lidar',
                type='lidar'
            ),
            timestamp=Decimal('1632321743.134149000')
        )
    },
    data={
        'velocity': 30.5,
        'longitude': 53.2356567,
        'latitude': 56.1254524
    },
    obects={}
)
```

### **StreamStamp**
The timestamp of a stream in a specific frame. Used for synchronization.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| stream | False | [raillabel.format.Stream](#stream) | The stream this StreamStamp corresponds to. |
| timestamp | False | [decimal.Decimal](https://docs.python.org/3/library/decimal.html#decimal.Decimal) | Timestamp containing the Unix epoch time of the stream in a specific frame with up to nanosecond precision. |

**Example:**
``` Python
import raillabel

stream_rgb_left = raillabel.format.Stream(
    uid='rgb_left',
    type='camera',
    rostopic='/rgb_left/image',
    description='Just some RGB camera on the left.'
)

stream_stamp = raillabel.format.StreamStamp(
    stream=stream_rgb_left,
    timestamp=Decimal('1632321743.100000072')
)
```

### **ObjectAnnotations**
Annotations associated with a specific object in a frame grouped by annotatione type.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| object | False | [raillabel.format.Object](#object) | A reference to the object this ObjectData belongs to. |
| bboxs | True | dict of [raillabel.format.Bbox](#bbox) | Dictionary of all bounding boxes representing this object in this frame. Default is {}. |
| cuboids | True | dict of [raillabel.format.Cuboid](#cuboid) | Dictionary of all cuboids representing this object in this frame. Default is {}. |
| poly2ds | True | dict of [raillabel.format.Poly2d](#poly2d) | Dictionary of all polylines representing this object in this frame. Default is {}. |
| seg3ds | True | dict of [raillabel.format.Seg3d](#seg3d) | Dictionary of all 3d segmentations representing this object in this frame. Default is {}. |

**Example:**
``` Python
import raillabel

obj = raillabel.format.ObjectAnnotations(
    uid='6fe55546-0dd7-4e40-b6b4-bb7ea3445772',
    name='person_0000',
    type='person'
)

obj_ann = raillabel.format.Object(
    object=obj,
    bboxs={
        '78f0ad89-2750-4a30-9d66-44c9da73a714': raillabel.format.Bbox(
            uid='78f0ad89-2750-4a30-9d66-44c9da73a714',
            pos=raillabel.format.Point2d(
                x=232,
                y=56
            ),
            size=raillabel.format.Size2d(
                x=39,
                y=32
            ),
            uri='example_file.png',
            coordinate_system=raillabel.format.CoordinateSystem(
                uid='rgb_left',
                type='sensor',
                parent=None,
                children=[]
            ),
            attributes={
                'is_an_example': True,
                'test_num': 420,
                'test_str': 'abc'
            }
        )
    },
    cuboids={
        'dc2be700-8ee4-45c4-9256-920b5d55c917': raillabel.format.Cuboid(
            uid='dc2be700-8ee4-45c4-9256-920b5d55c917',
            pos=raillabel.format.Point3d(13, 2.4, 0.2),
            quat=raillabel.format.Quaternion(0, 0, 0, 1),
            size=raillabel.format.Size3d(0.75, 0.75, 2),
            uri='example_file.pcd',
            coordinate_system=raillabel.format.CoordinateSystem(
                uid='rgb_left',
                type='sensor',
                parent=None,
                children=[]
            )
            attributes={
                'is_an_example': True,
                'test_num': 420,
                'test_str': 'abc'
            }
        )
    }
)
```

### **Bbox**
A 2D bounding box in an image.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| uid | False | str | This a string representing the unique universal identifier for the annotation. |
| pos | False | [raillabel.format.Point2d](#point2d) | The center point of the bbox in pixels. |
| size | False | [raillabel.format.Size2d](#size2d) | The dimensions of the bbox in pixels from the top left corner to the bottom right corner. |
| uri | True | str | The URI to the file, which contains the annotated object. Default is None. |
| attributes | True | dict | Attributes of the annotation. Dict keys are the name str of the attribute, values are the attribute values. Default is {}. |
| coordinate_system | True | [raillabel.format.CoordinateSystem](#coordinatesystem) | A reference to the coordinate_system, this annotation is labeled in. Default is None. |

**Example:**
``` Python
import raillabel

bbox = raillabel.format.Bbox(
    uid='78f0ad89-2750-4a30-9d66-44c9da73a714',
    pos=raillabel.format.Point2d(
        x=232,
        y=56
    ),
    size=raillabel.format.Size2d(
        x=39,
        y=32
    ),
    uri='example_file.png',
    coordinate_system=raillabel.format.CoordinateSystem(
        uid='rgb_left',
        type='sensor',
        parent=None,
        children=[]
    ),
    attributes={
        'is_an_example': True,
        'test_num': 420,
        'test_str': 'abc'
    }
)
```

### **Poly2d**
A 2D polyline defined as a sequence of 2D points. This class can either represent a polyline or a polygon, defined via the closed attribute.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| uid | False | str | This a string representing the unique universal identifier for the annotation. |
| points | False | list of [raillabel.format.Point2d](#point2d) | List of the 2d points that make up the polyline. |
| closed | False | bool | This parameter states, whether the polyline represents a closed shape (a polygon) or an open line. |
| mode | True | str | Mode of the polyline list of values: "MODE_POLY2D_ABSOLUTE" determines that the poly2d list contains the sequence of (x, y) values of all points of the polyline. "MODE_POLY2D_RELATIVE" specifies that only the first point of the sequence is defined with its (x, y) values, while all the rest are defined relative to it. "MODE_POLY2D_SRF6DCC" specifies that SRF6DCC chain code method is used. "MODE_POLY2D_RS6FCC" specifies that the RS6FCC method is used. Default is 'MODE_POLY2D_ABSOLUTE'. |
| uri | True | str | The URI to the file, which contains the annotated object. Default is None. |
| attributes | True | dict | Attributes of the annotation. Dict keys are the name str of the attribute, values are the attribute values. Default is {}. |
| coordinate_system | True | [raillabel.format.CoordinateSystem](#coordinatesystem) | A reference to the coordinate_system, this annotation is labeled in. Default is None. |

**Example:**
``` Python
import raillabel

polyline = raillabel.format.Poly2d(
    uid='bebfbae4-61a2-4758-993c-efa846b050a5',
    points=[
        raillabel.format.Point2d(232, 56),
        raillabel.format.Point2d(235, 21),
        raillabel.format.Point2d(232, 15)
    ],
    closed=False,
    mode='MODE_POLY2D_ABSOLUTE',
    uri='example_file.png',
    attributes={
        'is_an_example': True,
        'test_num': 420,
        'test_str': 'abc'
    }
)

polygon = raillabel.format.Poly2d(
    uid='3f63201c-fb33-4487-aff6-ae0aa5fa976c',
    points=[
        raillabel.format.Point2d(232, 56),
        raillabel.format.Point2d(235, 21),
        raillabel.format.Point2d(232, 15)
    ],
    closed=True,
    mode='MODE_POLY2D_ABSOLUTE',
    uri='example_file.png',
    attributes={
        'is_an_example': True,
        'test_num': 420,
        'test_str': 'abc'
    }
)
```

### **Cuboid**
A cuboid or 3D bounding box. It is defined by the position of its center, the rotation in 3D, and its dimensions.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| uid | False | str | This a string representing the unique universal identifier for the annotation. |
| pos | False | [raillabel.format.Point3d](#point3d) | The center position of the cuboid in meters, where the x coordinate points ahead of the vehicle, y points to the left and z points upwards. |
| quat | False | [raillabel.format.Quaternion](#quaternion) | The rotation of the cuboid in quaternions. |
| size | False | [raillabel.format.Size3d](#size3d) | The size of the cuboid in meters. |
| uri | True | str | The URI to the file, which contains the annotated object. Default is None. |
| attributes | True | dict | Attributes of the annotation. Dict keys are the name str of the attribute, values are the attribute values. Default is {}. |
| coordinate_system | True | [raillabel.format.CoordinateSystem](#coordinatesystem) | A reference to the coordinate_system, this annotation is labeled in. Default is None. |

**Example:**
``` Python
import raillabel

cuboid = raillabel.format.Cuboid(
    uid='dc2be700-8ee4-45c4-9256-920b5d55c917',
    pos=raillabel.format.Point3d(13, 2.4, 0.2),
    quat=raillabel.format.Quaternion(0, 0, 0, 1),
    size=raillabel.format.Size3d(0.75, 0.75, 2),
    uri='example_file.pcd',
    coordinate_system=raillabel.format.CoordinateSystem(
        uid='rgb_left',
        type='sensor',
        parent=None,
        children=[]
    )
    attributes={
        'is_an_example': True,
        'test_num': 420,
        'test_str': 'abc'
    }
)
```

### **Seg3d**
A 2D bounding box in an image.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| uid | False | str | This a string representing the unique universal identifier for the annotation. |
| point_ids | False | list of int | The list of point indices. |
| uri | True | str | The URI to the file, which contains the annotated object. Default is None. |
| attributes | True | dict | Attributes of the annotation. Dict keys are the name str of the attribute, values are the attribute values. Default is {}. |
| coordinate_system | True | [raillabel.format.CoordinateSystem](#coordinatesystem) | A reference to the coordinate_system, this annotation is labeled in. Default is None. |

**Example:**
``` Python
import raillabel

seg3d = raillabel.format.Seg3d(
    uid='c1087f1d-7271-4dee-83ad-519a4e3b78a8',
    point_ids=[
        2103,
        2104,
        2105
    ],
    uri='example_file.pcd',
    coordinate_system=raillabel.format.CoordinateSystem(
        uid='rgb_left',
        type='sensor',
        parent=None,
        children=[]
    )
    attributes={
        'is_an_example': True,
        'test_num': 420,
        'test_str': 'abc'
    }
)
```

### **Num**
A number.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| uid | False | str | This a string representing the unique universal identifier for the annotation. |
| val | False | float or int | The number value |
| uri | True | str | The URI to the file, which contains the annotated object. Default is None. |
| attributes | True | dict | Attributes of the annotation. Dict keys are the name str of the attribute, values are the attribute values. Default is {}. |
| coordinate_system | True | [raillabel.format.CoordinateSystem](#coordinatesystem) | A reference to the coordinate_system, this annotation is labeled in. Default is None. |

**Example:**
``` Python
import raillabel

num = raillabel.format.Num(
    uid='4b3ef402-eadc-468e-ac81-c20b401a68e2',
    val=13.456,
    uri='example_file.csv',
    coordinate_system=raillabel.format.CoordinateSystem(
        uid='gps_imu',
        type='sensor',
        parent=None,
        children=[]
    )
    attributes={
        'is_an_example': True,
        'test_num': 420,
        'test_str': 'abc'
    }
)
```

### **Point2d**
A 2d point in an image.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| x | False | float | The x-coordinate of the point in the image. |
| y | False | float | The y-coordinate of the point in the image. |

**Example:**
``` Python
import raillabel

p = raillabel.format.Point2d(
    x=5,
    y=12
)
```

### **Size2d**
The size of a rectangle in a 2d image.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| x | False | float | The size along the x-axis. |
| y | False | float | The size along the y-axis. |

**Example:**
``` Python
import raillabel

s = raillabel.format.Size2d(
    x=51,
    y=24
)
```

### **Point3d**
A point in the 3D space.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| x | False | float | The x-coordinate of the point. |
| y | False | float | The y-coordinate of the point. |
| z | False | float | The z-coordinate of the point. |

**Example:**
``` Python
import raillabel

p = raillabel.format.Point3d(
    x=5,
    y=12,
    z=1
)
```

### **Size3d**
The 3D size of a cube.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| x | False | float | The size along the x-axis. |
| y | False | float | The size along the y-axis. |
| z | False | float | The size along the z-axis. |

**Example:**
``` Python
import raillabel

s = raillabel.format.Size3d(
    x=0.75,
    y=0.75,
    z=2
)
```

### **Quaternion**
A quaternion.

**Parameters:**
| Name | Optional | Type | Description |
|------|----------|------|-------------|
| x | False | float | The x component of the quaternion. |
| y | False | float | The y component of the quaternion. |
| z | False | float | The z component of the quaternion. |
| w | False | float | The w component of the quaternion. |

**Example:**
``` Python
import raillabel

q = raillabel.format.Quaternion(
    x=0,
    y=0,
    z=0,
    w=1
)
```
