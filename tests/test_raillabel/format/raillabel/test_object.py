# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import random
import sys
import typing as t
from pathlib import Path
from uuid import UUID, uuid4

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel._util._attribute_type import AttributeType
from raillabel.format import (
    Bbox,
    Cuboid,
    Frame,
    FrameInterval,
    Object,
    Point2d,
    Point3d,
    Quaternion,
    Sensor,
    Size2d,
    Size3d,
)

# == Fixtures =========================

@pytest.fixture
def objects_dict(object_person_dict, object_train_dict) -> dict:
    return {
        object_person_dict["object_uid"]: object_person_dict["data_dict"],
        object_train_dict["object_uid"]: object_train_dict["data_dict"],
    }

@pytest.fixture
def objects(object_person, object_train) -> t.Dict[str, Object]:
    return {
        object_person.uid: object_person,
        object_train.uid: object_train,
    }


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


@pytest.fixture
def object_train_dict() -> dict:
    return {
        "object_uid": "d51a19be-8bc2-4a82-b66a-03c8de95b0cf",
        "data_dict": {
            "name": "train_0000",
            "type": "train",
        },
    }

@pytest.fixture
def object_train() -> dict:
    return Object(
        uid="d51a19be-8bc2-4a82-b66a-03c8de95b0cf",
        name="train_0000",
        type="train",
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


def test_asdict_no_frames():
    object = Object(
        uid="b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        name="person_0000",
        type="person",
    )

    assert object.asdict() == {
        "name": "person_0000",
        "type": "person",
    }

def test_asdict_with_frames():
    object = Object(
        uid="b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        name="person_0000",
        type="person",
    )

    frames = {
        0: build_frame(0,
            {
                object: [build_annotation("rgb_middle__bbox__person", object)]
            }
        ),
    }

    object_dict = object.asdict(frames)

    assert "frame_intervals" in object_dict
    assert "object_data_pointers" in object_dict
    assert "rgb_middle__bbox__person" in object_dict["object_data_pointers"]


def test_frame_intervals():
    object = Object(
        uid="b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        name="person_0000",
        type="person",
    )

    frames = {
        0: build_frame(0, {object: [build_annotation("rgb_middle__bbox__person", object)]}),
        1: build_frame(1, {object: [build_annotation("rgb_middle__bbox__person", object)]}),
        2: build_frame(2, {}),
        3: build_frame(3, {object: [build_annotation("rgb_middle__bbox__person", object)]}),
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
                    build_annotation("rgb_middle__bbox__person", object),
                    build_annotation("lidar__bbox__person", object)
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
                    build_annotation("rgb_middle__bbox__person", object),
                    build_annotation("rgb_middle__cuboid__person", object)
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
                object: [build_annotation("rgb_middle__bbox__person", object)]
            }
        ),
        1: build_frame(1,
            {
                object: [build_annotation("rgb_middle__bbox__person", object)]
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
                object: [build_annotation("rgb_middle__bbox__person", object)]
            }
        ),
        1: build_frame(1,
            {
                object: [build_annotation("rgb_middle__bbox__person", object)]
            }
        ),
        8: build_frame(8,
            {
                object: [build_annotation("rgb_middle__bbox__person", object)]
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
                        object=object,
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
                        object=object,
                        attributes={
                            "text_attr": "some value",
                            "num_attr": 0,
                        }
                    ),
                    build_annotation(
                        name="rgb_middle__bbox__person",
                        object=object,
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
                    build_annotation("lidar__bbox__person", object_person),
                ]
            }
        ),
        1: build_frame(1,
            {
                object_train: [
                    build_annotation("lidar__bbox__train", object_train),
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
                    build_annotation("lidar__bbox__person", object1),
                ]
            }
        ),
        1: build_frame(1,
            {
                object2: [
                    build_annotation("lidar__bbox__person", object2),
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

def build_annotation(name: str, object: Object, attributes: dict={}) -> t.Union[Bbox, Cuboid]:
    sensor_uid, ann_type, object_type = tuple(name.split("__"))

    sensor = Sensor(sensor_uid)

    if ann_type == "bbox":
        return Bbox(
            uid=str(uuid4()),
            object=object,
            attributes=attributes,
            sensor=sensor,
            pos=Point2d(50, 100),
            size=Size2d(30, 30)
        )

    elif ann_type == "cuboid":
        return Cuboid(
            uid=str(uuid4()),
            object=object,
            attributes=attributes,
            sensor=sensor,
            pos=Point3d(50, 100, 20),
            size=Size3d(30, 30, 30),
            quat=Quaternion(0, 0, 0, 1),
        )

    else:
        raise ValueError()

def build_frame(uid: int, raw_object_data: t.Dict[Object, t.List[t.Union[Bbox, Cuboid]]]) -> Frame:
    annotations = {}
    for object, object_data in raw_object_data.items():
        for annotation in object_data:
            annotations[annotation.uid] = annotation

    return Frame(uid=uid, annotations=annotations)

def build_object(type: str) -> Object:
    return Object(
        uid=str(uuid4()),
        name=f"{type}_{str(random.randint(0, 9999)).zfill(4)}",
        type=type
    )

if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
