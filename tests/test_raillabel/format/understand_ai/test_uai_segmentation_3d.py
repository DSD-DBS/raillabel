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
def segmentation_3d_uai_dict(sensor_lidar_uai_dict, attributes_uai_dict) -> dict:
    return {
        "id": "13478f94-d556-4f64-a72b-47662e94988e",
        "objectId": "05a7e7a7-91e1-49ef-a172-780f2461f013",
        "className": "test_class",
        "geometry": {
            "associatedPoints": [39814, 39815, 39816, 39817, 39818],
            "numberOfPointsInBox": 5
        },
        "attributes": attributes_uai_dict,
        "sensor": sensor_lidar_uai_dict,
    }

@pytest.fixture
def segmentation_3d_uai(attributes_uai, sensor_lidar_uai) -> dict:
    return uai_format.Segmentation3d(
        id=UUID("13478f94-d556-4f64-a72b-47662e94988e"),
        object_id=UUID("05a7e7a7-91e1-49ef-a172-780f2461f013"),
        class_name="test_class",
        associated_points=[39814, 39815, 39816, 39817, 39818],
        number_of_points=5,
        attributes=attributes_uai,
        sensor=sensor_lidar_uai,
    )

@pytest.fixture
def segmentation_3d_raillabel_dict(attributes_raillabel_dict, coordinate_system_lidar_translated_uid) -> dict:
    return {
        "name": "13478f94-d556-4f64-a72b-47662e94988e",
        "val": [39814, 39815, 39816, 39817, 39818],
        "coordinate_system": coordinate_system_lidar_translated_uid,
        "attributes": attributes_raillabel_dict
    }

# == Tests ============================

def test_fromdict(
    attributes_uai_dict, attributes_uai,
    sensor_lidar_uai_dict, sensor_lidar_uai
):
    segmentation_3d = uai_format.Segmentation3d.fromdict(
        {
            "id": "13478f94-d556-4f64-a72b-47662e94988e",
            "objectId": "05a7e7a7-91e1-49ef-a172-780f2461f013",
            "className": "test_class",
            "geometry": {
                "associatedPoints": [39814, 39815, 39816, 39817, 39818],
                "numberOfPointsInBox": 5
            },
            "attributes": attributes_uai_dict,
            "sensor": sensor_lidar_uai_dict,
        }
    )

    assert segmentation_3d.id == UUID("13478f94-d556-4f64-a72b-47662e94988e")
    assert segmentation_3d.object_id == UUID("05a7e7a7-91e1-49ef-a172-780f2461f013")
    assert segmentation_3d.class_name == "test_class"
    assert segmentation_3d.associated_points == [39814, 39815, 39816, 39817, 39818]
    assert segmentation_3d.number_of_points == 5
    assert segmentation_3d.attributes == attributes_uai
    assert segmentation_3d.sensor == sensor_lidar_uai


def test_to_raillabel(
    attributes_uai, attributes_raillabel_dict,
    sensor_lidar_uai, sensor_lidar_raillabel_dict, coordinate_system_lidar_translated_uid,
):
    segmentation_3d = uai_format.Segmentation3d(
        id=UUID("13478f94-d556-4f64-a72b-47662e94988e"),
        object_id=UUID("05a7e7a7-91e1-49ef-a172-780f2461f013"),
        class_name="test_class",
        associated_points=[39814, 39815, 39816, 39817, 39818],
        number_of_points=5,
        attributes=attributes_uai,
        sensor=sensor_lidar_uai,
    )

    data_dict, object_id, translated_class_id, sensor_reference = segmentation_3d.to_raillabel()

    assert data_dict == {
        "name": "13478f94-d556-4f64-a72b-47662e94988e",
        "val": [39814, 39815, 39816, 39817, 39818],
        "coordinate_system": coordinate_system_lidar_translated_uid,
        "attributes": attributes_raillabel_dict,
    }
    assert object_id == str(segmentation_3d.object_id)
    assert translated_class_id == translate_class_id(segmentation_3d.class_name)
    assert sensor_reference == sensor_lidar_raillabel_dict

if __name__ == "__main__":
    import os
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
