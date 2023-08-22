# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import random
import sys
import typing as t
from pathlib import Path
from uuid import UUID, uuid4

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel._util._attribute_type import AttributeType
from raillabel.format import (
    Bbox,
    Cuboid,
    Frame,
    FrameInterval,
    Object,
    ObjectData,
    Point2d,
    Point3d,
    Quaternion,
    Sensor,
    Size2d,
    Size3d,
)

# == Fixtures =========================

@pytest.fixture
def object_person_dict() -> dict:
    return {
        "object_uid": "b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        "data_dict": {
            "name": "person_0000",
            "type": "person",
        },
    }

@pytest.fixture
def object_person() -> dict:
    return Object(
        uid="b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        name="person_0000",
        type="person",
    )

# == Tests ============================

def test_fromdict():
    object = Object.fromdict(
        object_uid="b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        data_dict={
            "name": "person_0000",
            "type": "person",
        }
    )

    assert object.uid == "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    assert object.name == "person_0000"
    assert object.type == "person"


def test_asdict():
    object = Object(
        uid="b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        name="person_0000",
        type="person",
    )

    assert object.asdict() == {
        "name": "person_0000",
        "type": "person",
    }


def test_frame_intervals():
    object = Object(
        uid="b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        name="person_0000",
        type="person",
    )

    frames = {
        0: Frame(
            uid=0,
            object_data={UUID(object.uid): None}
        ),
        1: Frame(
            uid=1,
            object_data={UUID(object.uid): None}
        ),
        2: Frame(
            uid=2,
            object_data={}
        ),
        3: Frame(
            uid=3,
            object_data={UUID(object.uid): None}
        ),
    }

    assert object.frame_intervals(frames) == [
        FrameInterval(0, 1),
        FrameInterval(3, 3),
    ]


def test_object_data_pointers__sensor():
    object = build_object("person")

    frames = {
        0: build_frame(0,
            {
                object: [
                    build_annotation("rgb_middle__bbox__person"),
                    build_annotation("lidar__bbox__person")
                ]
            }
        )
    }

    object_data_pointers = object.object_data_pointers(frames)

    assert set(object_data_pointers.keys()) == set(["rgb_middle__bbox__person", "lidar__bbox__person"])

def test_object_data_pointers__annotation_type():
    object = build_object("person")

    frames = {
        0: build_frame(0,
            {
                object: [
                    build_annotation("rgb_middle__bbox__person"),
                    build_annotation("rgb_middle__cuboid__person")
                ]
            }
        )
    }

    object_data_pointers = object.object_data_pointers(frames)

    assert set(object_data_pointers.keys()) == set([
        "rgb_middle__bbox__person",
        "rgb_middle__cuboid__person"
    ])

def test_object_data_pointers__one_frame_interval():
    object = build_object("person")

    frames = {
        0: build_frame(0,
            {
                object: [build_annotation("rgb_middle__bbox__person")]
            }
        ),
        1: build_frame(1,
            {
                object: [build_annotation("rgb_middle__bbox__person")]
            }
        ),
    }

    object_data_pointers = object.object_data_pointers(frames)

    assert len(object_data_pointers) == 1
    assert object_data_pointers["rgb_middle__bbox__person"].frame_intervals == [
        FrameInterval(0, 1)
    ]

def test_object_data_pointers__two_frame_intervals():
    object = build_object("person")

    frames = {
        0: build_frame(0,
            {
                object: [build_annotation("rgb_middle__bbox__person")]
            }
        ),
        1: build_frame(1,
            {
                object: [build_annotation("rgb_middle__bbox__person")]
            }
        ),
        8: build_frame(8,
            {
                object: [build_annotation("rgb_middle__bbox__person")]
            }
        ),
    }

    object_data_pointers = object.object_data_pointers(frames)

    assert len(object_data_pointers) == 1
    assert object_data_pointers["rgb_middle__bbox__person"].frame_intervals == [
        FrameInterval(0, 1),
        FrameInterval(8, 8),
    ]

def test_object_data_pointers__attributes_one_annotation():
    object = build_object("person")

    frames = {
        0: build_frame(0,
            {
                object: [
                    build_annotation(
                        name="rgb_middle__bbox__person",
                        attributes={
                            "text_attr": "some value",
                            "num_attr": 0,
                            "bool_attr": True,
                            "vec_attr": [0, 1],
                        }
                    ),
                ]
            }
        )
    }

    object_data_pointers = object.object_data_pointers(frames)

    assert object_data_pointers["rgb_middle__bbox__person"].attribute_pointers == {
        "text_attr": AttributeType.TEXT,
        "num_attr": AttributeType.NUM,
        "bool_attr": AttributeType.BOOLEAN,
        "vec_attr": AttributeType.VEC,
    }

def test_object_data_pointers__attributes_multiple_annotations_with_differing_attributes():
    object = build_object("person")

    frames = {
        0: build_frame(0,
            {
                object: [
                    build_annotation(
                        name="rgb_middle__bbox__person",
                        attributes={
                            "text_attr": "some value",
                            "num_attr": 0,
                        }
                    ),
                    build_annotation(
                        name="rgb_middle__bbox__person",
                        attributes={
                            "bool_attr": True,
                            "vec_attr": [0, 1],
                        }
                    ),
                ]
            }
        )
    }

    object_data_pointers = object.object_data_pointers(frames)

    assert object_data_pointers["rgb_middle__bbox__person"].attribute_pointers == {
        "text_attr": AttributeType.TEXT,
        "num_attr": AttributeType.NUM,
        "bool_attr": AttributeType.BOOLEAN,
        "vec_attr": AttributeType.VEC,
    }

def test_object_data_pointers__multiple_objects_of_differing_type():
    object_person = build_object("person")
    object_train = build_object("train")

    frames = {
        0: build_frame(0,
            {
                object_person: [
                    build_annotation("lidar__bbox__person"),
                ]
            }
        ),
        1: build_frame(1,
            {
                object_train: [
                    build_annotation("lidar__bbox__train"),
                ]
            }
        )
    }

    person_object_data_pointers = object_person.object_data_pointers(frames)
    assert len(person_object_data_pointers) == 1
    assert person_object_data_pointers["lidar__bbox__person"].frame_intervals == [
        FrameInterval(0, 0)
    ]

    train_object_data_pointers = object_train.object_data_pointers(frames)
    assert len(train_object_data_pointers) == 1
    assert train_object_data_pointers["lidar__bbox__train"].frame_intervals == [
        FrameInterval(1, 1)
    ]

def test_object_data_pointers__multiple_objects_of_same_type():
    object1 = build_object("person")
    object2 = build_object("person")

    frames = {
        0: build_frame(0,
            {
                object1: [
                    build_annotation("lidar__bbox__person"),
                ]
            }
        ),
        1: build_frame(1,
            {
                object2: [
                    build_annotation("lidar__bbox__person"),
                ]
            }
        )
    }

    object1_data_pointers = object1.object_data_pointers(frames)
    assert len(object1_data_pointers) == 1
    assert object1_data_pointers["lidar__bbox__person"].frame_intervals == [
        FrameInterval(0, 0)
    ]

    object2_data_pointers = object2.object_data_pointers(frames)
    assert len(object2_data_pointers) == 1
    assert object2_data_pointers["lidar__bbox__person"].frame_intervals == [
        FrameInterval(1, 1)
    ]

# == Helpers ==========================

def build_annotation(name: str, attributes: dict={}) -> t.Union[Bbox, Cuboid]:
    sensor_uid, ann_type, object_type = tuple(name.split("__"))

    sensor = Sensor(sensor_uid)

    if ann_type == "bbox":
        return Bbox(
            uid=uuid4(),
            name=name,
            attributes=attributes,
            sensor=sensor,
            pos=Point2d(50, 100),
            size=Size2d(30, 30)
        )

    elif ann_type == "cuboid":
        return Cuboid(
            uid=uuid4(),
            name=name,
            attributes=attributes,
            sensor=sensor,
            pos=Point3d(50, 100, 20),
            size=Size3d(30, 30, 30),
            quat=Quaternion(0, 0, 0, 1),
        )

    else:
        raise ValueError()

def build_frame(uid: int, raw_object_data: t.Dict[Object, t.List[t.Union[Bbox, Cuboid]]]) -> Frame:
    object_data = {}
    for object, annotations in raw_object_data.items():
        object_data[object.uid] = ObjectData(
            object=object,
            annotations={ann.uid: ann for ann in annotations}
        )

    return Frame(uid=uid, object_data=object_data)

def build_object(type: str) -> Object:
    return Object(
        uid=uuid4(),
        name=f"{type}_{str(random.randint(0, 9999)).zfill(4)}",
        type=type
    )

if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
