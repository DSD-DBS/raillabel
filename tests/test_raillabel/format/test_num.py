# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel.format.num import Num

# == Fixtures =========================

@pytest.fixture
def num_dict(sensor_camera, attributes_multiple_types_dict) -> dict:
    return {
        "uid": "4e86c449-3B19-410c-aa64-603d46da3b26",
        "name": "rgb_middle__num__whatever",
        "val": 24,
        "coordinate_system": sensor_camera.uid,
        "attributes": attributes_multiple_types_dict
    }

@pytest.fixture
def num(sensor_camera, attributes_multiple_types) -> dict:
    return Num(
        uid="4e86c449-3B19-410c-aa64-603d46da3b26",
        name="rgb_middle__num__whatever",
        val=24,
        sensor=sensor_camera,
        attributes=attributes_multiple_types,
    )

# == Tests ============================

def test_fromdict(
    sensor_camera,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    num = Num.fromdict(
        {
            "uid": "4e86c449-3B19-410c-aa64-603d46da3b26",
            "name": "rgb_middle__num__whatever",
            "val": 24,
            "coordinate_system": sensor_camera.uid,
            "attributes": attributes_multiple_types_dict
        },
        {
            sensor_camera.uid: sensor_camera
        }
    )

    assert num.uid == "4e86c449-3B19-410c-aa64-603d46da3b26"
    assert num.name == "rgb_middle__num__whatever"
    assert num.val == 24
    assert num.sensor == sensor_camera
    assert num.attributes == attributes_multiple_types


def test_asdict(
    sensor_camera,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    num = Num(
        uid="4e86c449-3B19-410c-aa64-603d46da3b26",
        name="rgb_middle__num__whatever",
        val=24,
        sensor=sensor_camera,
        attributes=attributes_multiple_types,
    )

    assert num.asdict() == {
        "uid": "4e86c449-3B19-410c-aa64-603d46da3b26",
        "name": "rgb_middle__num__whatever",
        "val": 24,
        "coordinate_system": sensor_camera.uid,
        "attributes": attributes_multiple_types_dict
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
