# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel._util._warning import _WarningsLogger
from raillabel.format import Frame

# == Fixtures =========================

@pytest.fixture
def frame_dict(
    sensor_reference_camera_dict,
    num_dict,
    object_person, object_data_person_dict,
    object_train, object_data_train_dict,
) -> dict:
    return {
        "frame_properties": {
            "timestamp": "1632321743.100000072",
            "streams": {
                "rgb_middle": sensor_reference_camera_dict
            },
            "frame_data": {
                "num": [num_dict]
            },
        },
        "objects": {
            object_person.uid: object_data_person_dict,
            object_train.uid: object_data_train_dict,
        }
    }

@pytest.fixture
def frame(
    sensor_reference_camera,
    num,
    all_annotations
) -> dict:
    return Frame(
        uid=0,
        timestamp=Decimal("1632321743.100000072"),
        sensors={sensor_reference_camera.sensor.uid: sensor_reference_camera},
        frame_data={num.name: num},
        annotations=all_annotations
    )

# == Tests ============================

def test_fromdict_sensors(
    sensor_reference_camera_dict,
    sensor_reference_camera,
    sensor_camera
):
    frame = Frame.fromdict(
        uid=0,
        data_dict={
            "frame_properties": {
                "timestamp": "1632321743.100000072",
                "streams": {
                    "rgb_middle": sensor_reference_camera_dict
                }
            }
        },
        sensors={sensor_camera.uid: sensor_camera},
        objects={},
    )

    assert frame.uid == 0
    assert frame.timestamp == Decimal("1632321743.100000072")
    assert frame.sensors == {sensor_reference_camera.sensor.uid: sensor_reference_camera}

def test_fromdict_frame_data(
    num, num_dict,
    sensor_camera
):
    frame = Frame.fromdict(
        uid=1,
        data_dict={
            "frame_properties": {
                "frame_data": {
                    "num": [num_dict]
                }
            }
        },
        sensors={sensor_camera.uid: sensor_camera},
        objects={},
    )

    assert frame.frame_data == {num.name: num}

def test_fromdict_annotations(
    object_data_person_dict, object_person,
    object_data_train_dict, object_train,
    sensors,
    all_annotations,
):
    frame = Frame.fromdict(
        uid=2,
        data_dict={
            "objects": {
                object_person.uid: object_data_person_dict,
                object_train.uid: object_data_train_dict,
            }
        },
        sensors=sensors,
        objects={
            object_person.uid: object_person,
            object_train.uid: object_train,
        },
    )

    assert frame.annotations == all_annotations

def test_fromdict_uri_attribute(
    bbox_dict,
    sensor_reference_camera_dict, sensors,
    object_person, objects,
):
    bbox_with_uri_attribute = bbox_dict
    bbox_with_uri_attribute["attributes"]["text"].append({
        "name": "uri",
        "val": "test_uri.png"
    })

    with _WarningsLogger() as logger:
        frame = Frame.fromdict(
            uid=0,
            data_dict={
                "frame_properties": {
                    "streams": {
                        "rgb_middle": sensor_reference_camera_dict
                    }
                },
                "objects": {
                    object_person.uid: {
                        "object_data": {
                            "bbox": [bbox_with_uri_attribute]
                        }
                    }
                }
            },
            sensors=sensors,
            objects=objects,
        )

    assert len(logger.warnings) == 1
    assert "uri" in logger.warnings[0]
    assert bbox_with_uri_attribute["uid"] in logger.warnings[0]
    assert "raillabel.save()" in logger.warnings[0]

    assert frame.sensors["rgb_middle"].uri == "test_uri.png"
    assert "uri" not in frame.annotations[bbox_with_uri_attribute["uid"]].attributes

def test_fromdict_duplicate_annotation_uid_warning(
    sensors,
    object_person, objects,
    bbox_dict, cuboid_dict
):
    cuboid_dict["uid"] = bbox_dict["uid"]

    with _WarningsLogger() as logger:
        frame = Frame.fromdict(
            uid=2,
            data_dict={
                "objects": {
                    object_person.uid: {
                        "object_data": {
                            "bbox": [bbox_dict],
                            "cuboid": [cuboid_dict],
                        }
                    }
                }
            },
            sensors=sensors,
            objects=objects,
        )

    assert len(logger.warnings) == 1
    assert bbox_dict["uid"] in logger.warnings[0]
    assert list(frame.annotations.values())[0].uid != list(frame.annotations.values())[1].uid


def test_asdict_sensors(
    sensor_reference_camera_dict,
    sensor_reference_camera,
):
    frame = Frame(
        uid=0,
        timestamp=Decimal("1632321743.100000072"),
        sensors={sensor_reference_camera.sensor.uid: sensor_reference_camera},
    )

    assert frame.asdict() == {
        "frame_properties": {
            "timestamp": "1632321743.100000072",
            "streams": {
                "rgb_middle": sensor_reference_camera_dict
            }
        }
    }

def test_asdict_frame_data(num, num_dict):
    frame = Frame(
        uid=0,
        frame_data={num.name: num}
    )

    assert frame.asdict() == {
        "frame_properties": {
            "frame_data": {
                "num": [num_dict]
            }
        }
    }

def test_asdict_object_data(
    object_data_person_dict, object_person,
    object_data_train_dict, object_train,
    all_annotations
):
    frame = Frame(
        uid=0,
        annotations=all_annotations
    )

    assert frame.asdict() == {
        "objects": {
            object_person.uid: object_data_person_dict,
            object_train.uid: object_data_train_dict,
        }
    }


def test_object_data(
    object_person, object_train,
    bbox, cuboid, poly2d, poly3d, seg3d,
    bbox_train
):
    frame = Frame(
        uid=2,
        annotations={
            bbox.uid: bbox,
            poly2d.uid: poly2d,
            cuboid.uid: cuboid,
            poly3d.uid: poly3d,
            seg3d.uid: seg3d,
            bbox_train.uid: bbox_train,
        }
    )

    assert frame.object_data == {
        object_person.uid: {
            bbox.uid: bbox,
            poly2d.uid: poly2d,
            cuboid.uid: cuboid,
            poly3d.uid: poly3d,
            seg3d.uid: seg3d,
        },
        object_train.uid: {
            bbox_train.uid: bbox_train
        }
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-vv"])
