# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel.format.bbox import Bbox

# == Fixtures =========================

@pytest.fixture
def bbox_dict(sensor_camera, attributes_multiple_types_dict, point2d_dict, size2d_dict) -> dict:
    return {
        "uid": "78f0ad89-2750-4a30-9d66-44c9da73a714",
        "name": "rgb_middle__bbox__person",
        "val": point2d_dict + size2d_dict,
        "coordinate_system": sensor_camera.uid,
        "attributes": attributes_multiple_types_dict
    }

@pytest.fixture
def bbox(point2d, size2d, sensor_camera, attributes_multiple_types) -> dict:
    return Bbox(
        uid="78f0ad89-2750-4a30-9d66-44c9da73a714",
        name="rgb_middle__bbox__person",
        pos=point2d,
        size=size2d,
        sensor=sensor_camera,
        attributes=attributes_multiple_types,
    )

# == Tests ============================

def test_fromdict(
    point2d, point2d_dict,
    size2d, size2d_dict,
    sensor_camera,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    bbox = Bbox.fromdict(
        {
            "uid": "78f0ad89-2750-4a30-9d66-44c9da73a714",
            "name": "rgb_middle__bbox__person",
            "val": point2d_dict + size2d_dict,
            "coordinate_system": sensor_camera.uid,
            "attributes": attributes_multiple_types_dict
        },
        {
            sensor_camera.uid: sensor_camera
        }
    )

    assert bbox.uid == "78f0ad89-2750-4a30-9d66-44c9da73a714"
    assert bbox.name == "rgb_middle__bbox__person"
    assert bbox.pos == point2d
    assert bbox.size == size2d
    assert bbox.sensor == sensor_camera
    assert bbox.attributes == attributes_multiple_types


def test_asdict(
    point2d, point2d_dict,
    size2d, size2d_dict,
    sensor_camera,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    bbox = Bbox(
        uid="78f0ad89-2750-4a30-9d66-44c9da73a714",
        name="rgb_middle__bbox__person",
        pos=point2d,
        size=size2d,
        sensor=sensor_camera,
        attributes=attributes_multiple_types,
    )

    assert bbox.asdict() == {
        "uid": "78f0ad89-2750-4a30-9d66-44c9da73a714",
        "name": "rgb_middle__bbox__person",
        "val": point2d_dict + size2d_dict,
        "coordinate_system": sensor_camera.uid,
        "attributes": attributes_multiple_types_dict
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
