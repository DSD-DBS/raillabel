# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel.format.frame import Frame

# == Fixtures =========================

@pytest.fixture
def frame_sensors_dict(sensor_reference_camera_dict) -> dict:
    return {
        "frame_properties": {
            "timestamp": "1632321743.100000072",
            "streams": {
                "rgb_middle": sensor_reference_camera_dict
            }
        }
    }

@pytest.fixture
def frame_sensors(sensor_reference_camera) -> dict:
    return Frame(
        uid=0,
        timestamp=Decimal("1632321743.100000072"),
        sensors={sensor_reference_camera.sensor.uid: sensor_reference_camera},
    )


@pytest.fixture
def frame_frame_data_dict(num_dict) -> dict:
    return {
        "frame_properties": {
            "frame_data": {
                "num": [num_dict]
            }
        }
    }

@pytest.fixture
def frame_frame_data(num) -> dict:
    return Frame(
        uid=0,
        frame_data={num.name: num}
    )


@pytest.fixture
def frame_object_data_dict(
    object_data_person_dict, object_data_person,
    object_data_train_dict, object_data_train,
) -> dict:
    return {
        "objects": {
            object_data_person.object.uid: object_data_person_dict,
            object_data_train.object.uid: object_data_train_dict,
        }
    }

@pytest.fixture
def frame_object_data(object_data_person, object_data_train) -> dict:
    return Frame(
        uid=0,
        object_data={
            object_data_person.object.uid: object_data_person,
            object_data_train.object.uid: object_data_train,
        }
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
        uid=0,
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

def test_fromdict_object_data(
    object_data_person_dict, object_data_person,
    object_data_train_dict, object_data_train,
    sensors,
    object_person, object_train,
):
    frame = Frame.fromdict(
        uid=0,
        data_dict={
            "objects": {
                object_data_person.object.uid: object_data_person_dict,
                object_data_train.object.uid: object_data_train_dict,
            }
        },
        sensors=sensors,
        objects={
            object_person.uid: object_person,
            object_train.uid: object_train,
        },
    )

    assert frame.object_data[object_data_person.object.uid] == object_data_person
    assert frame.object_data[object_data_train.object.uid] == object_data_train


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
    object_data_person_dict, object_data_person,
    object_data_train_dict, object_data_train,
    sensors,
    object_person, object_train,
):
    frame = Frame(
        uid=0,
        object_data={
            object_data_person.object.uid: object_data_person,
            object_data_train.object.uid: object_data_train,
        }
    )

    assert frame.asdict() == {
        "objects": {
            object_data_person.object.uid: object_data_person_dict,
            object_data_train.object.uid: object_data_train_dict,
        }
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-vv"])
