# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

import raillabel.format.understand_ai as uai_format

# == Fixtures =========================

@pytest.fixture
def sensor_camera_uai_dict() -> dict:
    return {
        "type": "ir_middle",
        "uri": "A0001781_image/000_1632321843.100464760.png",
        "timestamp": "1632321843.100464760"
    }

@pytest.fixture
def sensor_camera_uai() -> dict:
    return uai_format.SensorReference(
        type="ir_middle",
        uri="A0001781_image/000_1632321843.100464760.png",
        timestamp=Decimal("1632321843.100464760"),
    )

@pytest.fixture
def sensor_camera_raillabel_dict() -> dict:
    return {
        "stream_properties": {
            "sync": {
                "timestamp": "1632321843.100464760"
            }
        },
        "uri": "000_1632321843.100464760.png"
    }


@pytest.fixture
def sensor_lidar_uai_dict() -> dict:
    return {
        "type": "LIDAR",
        "uri": "lidar_merged/000_1632321880.132833000.pcd",
        "timestamp": "1632321880.132833000"
    }

@pytest.fixture
def sensor_lidar_uai() -> dict:
    return uai_format.SensorReference(
        type="LIDAR",
        uri="lidar_merged/000_1632321880.132833000.pcd",
        timestamp=Decimal("1632321880.132833000"),
    )

@pytest.fixture
def sensor_lidar_raillabel_dict() -> dict:
    return {
        "stream_properties": {
            "sync": {
                "timestamp": "1632321880.132833000"
            }
        },
        "uri": "000_1632321880.132833000.pcd"
    }

# == Tests ============================

def test_fromdict():
    sensor_reference = uai_format.SensorReference.fromdict(
        {
            "type": "ir_middle",
            "uri": "A0001781_image/000_1632321843.100464760.png",
            "timestamp": "1632321843.100464760"
        }
    )

    assert sensor_reference.type == "ir_middle"
    assert sensor_reference.uri == "A0001781_image/000_1632321843.100464760.png"
    assert sensor_reference.timestamp == Decimal("1632321843.100464760")


def test_to_raillabel():
    sensor_reference = uai_format.SensorReference(
        type="ir_middle",
        uri="A0001781_image/000_1632321843.100464760.png",
        timestamp=Decimal("1632321843.100464760"),
    )

    assert sensor_reference.to_raillabel()[0] == "ir_middle"
    assert sensor_reference.to_raillabel()[1] == {
        "stream_properties": {
            "sync": {
                "timestamp": "1632321843.100464760"
            }
        },
        "uri": "000_1632321843.100464760.png"
    }

if __name__ == "__main__":
    import os
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
