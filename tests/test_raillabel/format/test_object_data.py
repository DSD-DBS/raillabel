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
            "vec": [seg3d_dict],
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


@pytest.fixture
def object_data_train_dict(bbox_train_dict) -> dict:
    return {
        "object_data": {
            "bbox": [bbox_train_dict],
        }
    }

@pytest.fixture
def object_data_train(object_train, bbox_train, poly2d, cuboid, poly3d, seg3d) -> dict:
    return ObjectData(
        object=object_train,
        annotations={
            bbox_train.uid: bbox_train,
        }
    )

# == Tests ============================

def test_fromdict(
    object_person,
    sensors,
    bbox, bbox_dict,
    poly2d, poly2d_dict,
    cuboid, cuboid_dict,
    poly3d, poly3d_dict,
    seg3d, seg3d_dict,
):
    object_data = ObjectData.fromdict(
        object=object_person,
        data_dict={
            "bbox": [bbox_dict],
            "poly2d": [poly2d_dict],
            "cuboid": [cuboid_dict],
            "poly3d": [poly3d_dict],
            "vec": [seg3d_dict],
        },
        sensors=sensors,
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