# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import sys
from pathlib import Path
from uuid import UUID

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

import raillabel.format.understand_ai as uai_format
from raillabel.format.understand_ai._translation import translate_class_id

# == Fixtures =========================

@pytest.fixture
def bounding_box_2d_uai_dict(sensor_camera_uai_dict, attributes_uai_dict) -> dict:
    return {
        "id": "2f2a1d7f-56d1-435c-a3ec-d6b8fdaaa965",
        "objectId": "48c988bd-76f1-423f-b46d-7e7acb859f31",
        "className": "test_class",
        "geometry": {
            "xMin": 1,
            "yMin": 2,
            "xMax": 3,
            "yMax": 4
        },
        "attributes": attributes_uai_dict,
        "sensor": sensor_camera_uai_dict
    }

@pytest.fixture
def bounding_box_2d_uai(attributes_uai, sensor_camera_uai) -> dict:
    return uai_format.BoundingBox2d(
        id=UUID("2f2a1d7f-56d1-435c-a3ec-d6b8fdaaa965"),
        object_id=UUID("48c988bd-76f1-423f-b46d-7e7acb859f31"),
        class_name="test_class",
        x_min=1,
        y_min=2,
        x_max=3,
        y_max=4,
        attributes=attributes_uai,
        sensor=sensor_camera_uai,
    )

@pytest.fixture
def bounding_box_2d_raillabel_dict(attributes_raillabel_dict, coordinate_system_camera_translated_uid) -> dict:
    return {
        "name": "2f2a1d7f-56d1-435c-a3ec-d6b8fdaaa965",
        "val": [
            2.0,
            3.0,
            2.0,
            2.0
        ],
        "coordinate_system": coordinate_system_camera_translated_uid,
        "attributes": attributes_raillabel_dict,
    }


# == Tests ============================

def test_fromdict(
    attributes_uai_dict, attributes_uai,
    sensor_camera_uai_dict, sensor_camera_uai
):
    bounding_box_2d = uai_format.BoundingBox2d.fromdict(
        {
            "id": "2f2a1d7f-56d1-435c-a3ec-d6b8fdaaa965",
            "objectId": "48c988bd-76f1-423f-b46d-7e7acb859f31",
            "className": "test_class",
            "geometry": {
                "xMin": 1,
                "yMin": 2,
                "xMax": 3,
                "yMax": 4
            },
            "attributes": attributes_uai_dict,
            "sensor": sensor_camera_uai_dict
        }
    )

    assert bounding_box_2d.id == UUID("2f2a1d7f-56d1-435c-a3ec-d6b8fdaaa965")
    assert bounding_box_2d.object_id == UUID("48c988bd-76f1-423f-b46d-7e7acb859f31")
    assert bounding_box_2d.class_name == "test_class"
    assert bounding_box_2d.x_min == 1
    assert bounding_box_2d.y_min == 2
    assert bounding_box_2d.x_max == 3
    assert bounding_box_2d.y_max == 4
    assert bounding_box_2d.attributes == attributes_uai
    assert bounding_box_2d.sensor == sensor_camera_uai


def test_to_raillabel(
    attributes_uai, attributes_raillabel_dict,
    sensor_camera_uai, sensor_camera_raillabel_dict, coordinate_system_camera_translated_uid,
):
    bounding_box_2d = uai_format.BoundingBox2d(
        id=UUID("2f2a1d7f-56d1-435c-a3ec-d6b8fdaaa965"),
        object_id=UUID("48c988bd-76f1-423f-b46d-7e7acb859f31"),
        class_name="test_class",
        x_min=1,
        y_min=2,
        x_max=3,
        y_max=4,
        attributes=attributes_uai,
        sensor=sensor_camera_uai,
    )

    data_dict, object_id, translated_class_id, sensor_reference = bounding_box_2d.to_raillabel()

    assert data_dict == {
        "name": "2f2a1d7f-56d1-435c-a3ec-d6b8fdaaa965",
        "val": [
            2.0,
            3.0,
            2.0,
            2.0
        ],
        "coordinate_system": coordinate_system_camera_translated_uid,
        "attributes": attributes_raillabel_dict,
    }
    assert object_id == str(bounding_box_2d.object_id)
    assert translated_class_id == translate_class_id(bounding_box_2d.class_name)
    assert sensor_reference == sensor_camera_raillabel_dict

if __name__ == "__main__":
    import os
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
