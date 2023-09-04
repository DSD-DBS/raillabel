# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import SensorReference

# == Fixtures =========================

@pytest.fixture
def sensor_reference_camera_dict() -> dict:
    return {
        "stream_properties": {
            "sync": {
                "timestamp": "1632321743.100000072"
            }
        },
        "uri": "rgb_test0.png"
    }

@pytest.fixture
def sensor_reference_camera(sensor_camera) -> dict:
    return SensorReference(
        sensor=sensor_camera,
        timestamp=Decimal("1632321743.100000072"),
        uri="rgb_test0.png"
    )

# == Tests ============================

def test_fromdict(sensor_camera):
    sensor_reference = SensorReference.fromdict(
        {
            "stream_properties": {
                "sync": {
                    "timestamp": "1632321743.100000072"
                }
            },
            "uri": "rgb_test0.png"
        },
        sensor_camera
    )

    assert sensor_reference.sensor == sensor_camera
    assert sensor_reference.timestamp == Decimal("1632321743.100000072")
    assert sensor_reference.uri == "rgb_test0.png"


def test_asdict(sensor_camera):
    sensor_reference = SensorReference(
        sensor=sensor_camera,
        timestamp=Decimal("1632321743.100000072"),
        uri="rgb_test0.png"
    )

    assert sensor_reference.asdict() == {
        "stream_properties": {
            "sync": {
                "timestamp": "1632321743.100000072"
            }
        },
        "uri": "rgb_test0.png"
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
