# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Num

# == Fixtures =========================

@pytest.fixture
def num_dict(sensor_camera) -> dict:
    return {
        "uid": "4e86c449-3B19-410c-aa64-603d46da3b26",
        "name": "some_number",
        "val": 24,
        "coordinate_system": sensor_camera.uid
    }

@pytest.fixture
def num(sensor_camera) -> dict:
    return Num(
        uid="4e86c449-3B19-410c-aa64-603d46da3b26",
        name="some_number",
        val=24,
        sensor=sensor_camera,
    )

# == Tests ============================

def test_fromdict(sensor_camera):
    num = Num.fromdict(
        {
            "uid": "4e86c449-3B19-410c-aa64-603d46da3b26",
            "name": "some_number",
            "val": 24,
            "coordinate_system": sensor_camera.uid,
        },
        {
            sensor_camera.uid: sensor_camera
        }
    )

    assert num.uid == "4e86c449-3B19-410c-aa64-603d46da3b26"
    assert num.name == "some_number"
    assert num.val == 24
    assert num.sensor == sensor_camera


def test_asdict(sensor_camera):
    num = Num(
        uid="4e86c449-3B19-410c-aa64-603d46da3b26",
        name="some_number",
        val=24,
        sensor=sensor_camera,
    )

    assert num.asdict() == {
        "uid": "4e86c449-3B19-410c-aa64-603d46da3b26",
        "name": "some_number",
        "val": 24,
        "coordinate_system": sensor_camera.uid,
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
