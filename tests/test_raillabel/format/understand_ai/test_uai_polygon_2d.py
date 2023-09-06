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
def polygon_2d_uai_dict(sensor_camera_uai_dict, attributes_uai_dict) -> dict:
    return {
        "id": "0f90cffa-2b6b-4e09-8fc2-527769a94e0a",
        "objectId": "58e7edd8-a7ee-4775-a837-e6dd375e8150",
        "className": "test_class",
        "geometry": {
            "points": [
                [127.71153737657284,  -0.3861000079676791],
                [127.4762636010818,  328.04436391207815],
                [115.77703250958459, 334.4789410124016],
                [115.01063176442402, 411.0810690770479],
            ]
        },
        "attributes": attributes_uai_dict,
        "sensor": sensor_camera_uai_dict
    }


@pytest.fixture
def polygon_2d_uai(attributes_uai, sensor_camera_uai) -> dict:
    return uai_format.Polygon2d(
        id=UUID("0f90cffa-2b6b-4e09-8fc2-527769a94e0a"),
        object_id=UUID("58e7edd8-a7ee-4775-a837-e6dd375e8150"),
        class_name="test_class",
        points=[
            (127.71153737657284,  -0.3861000079676791),
            (127.4762636010818,  328.04436391207815),
            (115.77703250958459, 334.4789410124016),
            (115.01063176442402, 411.0810690770479),
        ],
        attributes=attributes_uai,
        sensor=sensor_camera_uai,
    )

@pytest.fixture
def polygon_2d_raillabel_dict(attributes_raillabel_dict, coordinate_system_camera_translated_uid) -> dict:
    return {
        "name": "0f90cffa-2b6b-4e09-8fc2-527769a94e0a",
        "val": [
            127.71153737657284,  -0.3861000079676791,
            127.4762636010818,  328.04436391207815,
            115.77703250958459, 334.4789410124016,
            115.01063176442402, 411.0810690770479,
        ],
        "mode": "MODE_POLY2D_ABSOLUTE",
        "closed": True,
        "coordinate_system": coordinate_system_camera_translated_uid,
        "attributes": attributes_raillabel_dict,
    }


# == Tests ============================

def test_fromdict(
    attributes_uai_dict, attributes_uai,
    sensor_camera_uai_dict, sensor_camera_uai
):
    polygon_2d = uai_format.Polygon2d.fromdict(
        {
            "id": "0f90cffa-2b6b-4e09-8fc2-527769a94e0a",
            "objectId": "58e7edd8-a7ee-4775-a837-e6dd375e8150",
            "className": "test_class",
            "geometry": {
                "points": [
                    [127.71153737657284,  -0.3861000079676791],
                    [127.4762636010818,  328.04436391207815],
                    [115.77703250958459, 334.4789410124016],
                    [115.01063176442402, 411.0810690770479],
                ]
            },
            "attributes": attributes_uai_dict,
            "sensor": sensor_camera_uai_dict
        }
    )

    assert polygon_2d.id == UUID("0f90cffa-2b6b-4e09-8fc2-527769a94e0a")
    assert polygon_2d.object_id == UUID("58e7edd8-a7ee-4775-a837-e6dd375e8150")
    assert polygon_2d.class_name == "test_class"
    assert polygon_2d.points == [
        (127.71153737657284,  -0.3861000079676791),
        (127.4762636010818,  328.04436391207815),
        (115.77703250958459, 334.4789410124016),
        (115.01063176442402, 411.0810690770479),
    ]
    assert polygon_2d.attributes == attributes_uai
    assert polygon_2d.sensor == sensor_camera_uai


def test_to_raillabel(
    attributes_uai, attributes_raillabel_dict,
    sensor_camera_uai, sensor_camera_raillabel_dict, coordinate_system_camera_translated_uid,
):
    polygon_2d = uai_format.Polygon2d(
        id=UUID("0f90cffa-2b6b-4e09-8fc2-527769a94e0a"),
        object_id=UUID("58e7edd8-a7ee-4775-a837-e6dd375e8150"),
        class_name="test_class",
        points=[
            (127.71153737657284,  -0.3861000079676791),
            (127.4762636010818,  328.04436391207815),
            (115.77703250958459, 334.4789410124016),
            (115.01063176442402, 411.0810690770479),
        ],
        attributes=attributes_uai,
        sensor=sensor_camera_uai,
    )

    data_dict, object_id, translated_class_id, sensor_reference = polygon_2d.to_raillabel()

    assert data_dict == {
        "name": "0f90cffa-2b6b-4e09-8fc2-527769a94e0a",
        "val": [
            127.71153737657284,  -0.3861000079676791,
            127.4762636010818,  328.04436391207815,
            115.77703250958459, 334.4789410124016,
            115.01063176442402, 411.0810690770479,
        ],
        "mode": "MODE_POLY2D_ABSOLUTE",
        "coordinate_system": coordinate_system_camera_translated_uid,
        "closed": True,
        "attributes": attributes_raillabel_dict,
    }
    assert object_id == str(polygon_2d.object_id)
    assert translated_class_id == translate_class_id(polygon_2d.class_name)
    assert sensor_reference == sensor_camera_raillabel_dict

if __name__ == "__main__":
    import os
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
