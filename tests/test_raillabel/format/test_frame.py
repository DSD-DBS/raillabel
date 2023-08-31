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


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
