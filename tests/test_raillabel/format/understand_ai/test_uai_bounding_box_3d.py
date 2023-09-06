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
def bounding_box_3d_uai_dict(
    point_3d_uai_dict, size_3d_uai_dict, quaternion_uai_dict,
    sensor_lidar_uai_dict,
    attributes_uai_dict
) -> dict:
    return {
        "id": "910399ec-da3e-4d7e-be42-ef8e53e38ca6",
        "objectId": "48c988bd-76f1-423f-b46d-7e7acb859f31",
        "className": "test_class",
        "geometry": {
            "size": size_3d_uai_dict,
            "center": point_3d_uai_dict,
            "quaternion": quaternion_uai_dict
        },
        "attributes": attributes_uai_dict,
        "sensor": sensor_lidar_uai_dict,
    }


@pytest.fixture
def bounding_box_3d_uai(
    point_3d_uai, size_3d_uai, quaternion_uai,
    attributes_uai,
    sensor_lidar_uai
):
    return uai_format.BoundingBox3d(
        id=UUID("910399ec-da3e-4d7e-be42-ef8e53e38ca6"),
        object_id=UUID("48c988bd-76f1-423f-b46d-7e7acb859f31"),
        class_name="test_class",
        size=size_3d_uai,
        center=point_3d_uai,
        quaternion=quaternion_uai,
        attributes=attributes_uai,
        sensor=sensor_lidar_uai,
    )

@pytest.fixture
def bounding_box_3d_raillabel_dict(
    point_3d_vec, size_3d_vec, quaternion_vec,
    coordinate_system_lidar_translated_uid, attributes_raillabel_dict
) -> dict:
    return {
        "name": "910399ec-da3e-4d7e-be42-ef8e53e38ca6",
        "val": point_3d_vec + quaternion_vec + size_3d_vec,
        "coordinate_system": coordinate_system_lidar_translated_uid,
        "attributes": attributes_raillabel_dict
    }


# == Tests ============================

def test_fromdict(
    size_3d_uai_dict, point_3d_uai_dict, quaternion_uai_dict,
    size_3d_uai, point_3d_uai, quaternion_uai,
    sensor_lidar_uai_dict, sensor_lidar_uai,
    attributes_uai_dict, attributes_uai,
):
    bounding_box_3d = uai_format.BoundingBox3d.fromdict(
        {
            "id": "910399ec-da3e-4d7e-be42-ef8e53e38ca6",
            "objectId": "48c988bd-76f1-423f-b46d-7e7acb859f31",
            "className": "test_class",
            "geometry": {
                "size": size_3d_uai_dict,
                "center": point_3d_uai_dict,
                "quaternion": quaternion_uai_dict
            },
            "attributes": attributes_uai_dict,
            "sensor": sensor_lidar_uai_dict,
        }
    )

    assert bounding_box_3d.object_id == UUID("48c988bd-76f1-423f-b46d-7e7acb859f31")
    assert bounding_box_3d.id == UUID("910399ec-da3e-4d7e-be42-ef8e53e38ca6")
    assert bounding_box_3d.class_name == "test_class"
    assert bounding_box_3d.size == size_3d_uai
    assert bounding_box_3d.center == point_3d_uai
    assert bounding_box_3d.quaternion == quaternion_uai
    assert bounding_box_3d.attributes == attributes_uai
    assert bounding_box_3d.sensor == sensor_lidar_uai


def test_to_raillabel(
    size_3d_uai, point_3d_uai, quaternion_uai,
    point_3d_vec, quaternion_vec, size_3d_vec,
    attributes_uai, attributes_raillabel_dict,
    sensor_lidar_uai, coordinate_system_lidar_translated_uid, sensor_lidar_raillabel_dict,
):
    bounding_box_3d = uai_format.BoundingBox3d(
        id=UUID("910399ec-da3e-4d7e-be42-ef8e53e38ca6"),
        object_id=UUID("48c988bd-76f1-423f-b46d-7e7acb859f31"),
        class_name="test_class",
        size=size_3d_uai,
        center=point_3d_uai,
        quaternion=quaternion_uai,
        attributes=attributes_uai,
        sensor=sensor_lidar_uai,
    )

    data_dict, object_id, translated_class_id, sensor_reference = bounding_box_3d.to_raillabel()

    assert data_dict == {
        "name": "910399ec-da3e-4d7e-be42-ef8e53e38ca6",
        "val": point_3d_vec + quaternion_vec + size_3d_vec,
        "coordinate_system": coordinate_system_lidar_translated_uid,
        "attributes": attributes_raillabel_dict
    }
    assert object_id == str(bounding_box_3d.object_id)
    assert translated_class_id == translate_class_id(bounding_box_3d.class_name)
    assert sensor_reference == sensor_lidar_raillabel_dict

if __name__ == "__main__":
    import os
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
