# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel.format.object_data import ObjectData

# == Fixtures =========================

@pytest.fixture
def object_data_person_dict(bbox_dict, poly2d_dict, cuboid_dict, poly3d_dict, seg3d_dict) -> dict:
    return {
        "object_data": {
            "bbox": [bbox_dict],
            "poly2d": [poly2d_dict],
            "cuboid": [cuboid_dict],
            "poly3d": [poly3d_dict],
            "seg3d": [seg3d_dict],
        }
    }

@pytest.fixture
def object_data_person(object_person, bbox, poly2d, cuboid, poly3d, seg3d) -> dict:
    return ObjectData(
        object=object_person,
        annotations={
            bbox.uid: bbox,
            poly2d.uid: poly2d,
            cuboid.uid: cuboid,
            poly3d.uid: poly3d,
            seg3d.uid: seg3d,
        }
    )

# == Tests ============================

def test_fromdict(
    object_person, annotation_classes,
    sensor_camera, sensor_lidar,
    bbox, bbox_dict,
    poly2d, poly2d_dict,
    cuboid, cuboid_dict,
    poly3d, poly3d_dict,
    seg3d, seg3d_dict,
):

    objects = {object_person.uid: object_person}
    sensors = {
        sensor_lidar.uid: sensor_lidar,
        sensor_camera.uid: sensor_camera,
    }

    object_data = ObjectData.fromdict(
        uid=object_person.uid,
        data_dict={
            "bbox": [bbox_dict],
            "poly2d": [poly2d_dict],
            "cuboid": [cuboid_dict],
            "poly3d": [poly3d_dict],
            "seg3d": [seg3d_dict],
        },
        objects=objects,
        sensors=sensors,
        annotation_classes=annotation_classes,
    )

    assert object_data.object == object_person
    assert len(object_data.annotations) == 5
    assert object_data.annotations[bbox.uid] == bbox
    assert object_data.annotations[poly2d.uid] == poly2d
    assert object_data.annotations[cuboid.uid] == cuboid
    assert object_data.annotations[poly3d.uid] == poly3d
    assert object_data.annotations[seg3d.uid] == seg3d


def test_asdict(
    object_person,
    bbox, bbox_dict,
    poly2d, poly2d_dict,
    cuboid, cuboid_dict,
    poly3d, poly3d_dict,
    seg3d, seg3d_dict,
):
    object_data = ObjectData(
        object=object_person,
        annotations={
            bbox.uid: bbox,
            poly2d.uid: poly2d,
            cuboid.uid: cuboid,
            poly3d.uid: poly3d,
            seg3d.uid: seg3d,
        }
    )

    assert object_data.asdict() == {
        "object_data": {
            "bbox": [bbox_dict],
            "poly2d": [poly2d_dict],
            "cuboid": [cuboid_dict],
            "poly3d": [poly3d_dict],
            "vec": [seg3d_dict],
        }
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
