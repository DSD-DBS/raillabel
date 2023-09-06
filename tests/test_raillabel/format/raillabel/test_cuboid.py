# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Cuboid

# == Fixtures =========================

@pytest.fixture
def cuboid_dict(
    sensor_lidar,
    attributes_multiple_types_dict,
    point3d_dict,
    size3d_dict,
    quaternion_dict
) -> dict:
    return {
        "uid": "2c6b3de0-86c2-4684-b576-4cfd4f50d6ad",
        "name": "lidar__cuboid__person",
        "val": point3d_dict + quaternion_dict + size3d_dict,
        "coordinate_system": sensor_lidar.uid,
        "attributes": attributes_multiple_types_dict
    }

@pytest.fixture
def cuboid(
    point3d, size3d, quaternion,
    sensor_lidar,
    attributes_multiple_types,
    object_person
) -> dict:
    return Cuboid(
        uid="2c6b3de0-86c2-4684-b576-4cfd4f50d6ad",
        pos=point3d,
        quat=quaternion,
        size=size3d,
        object=object_person,
        sensor=sensor_lidar,
        attributes=attributes_multiple_types,
    )

# == Tests ============================

def test_fromdict(
    point3d, point3d_dict,
    size3d, size3d_dict,
    quaternion, quaternion_dict,
    sensor_lidar, sensors,
    object_person,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    cuboid = Cuboid.fromdict(
        {
            "uid": "2c6b3de0-86c2-4684-b576-4cfd4f50d6ad",
            "name": "lidar__cuboid__person",
            "val": point3d_dict + quaternion_dict + size3d_dict,
            "coordinate_system": sensor_lidar.uid,
            "attributes": attributes_multiple_types_dict
        },
        sensors,
        object_person
    )

    assert cuboid.uid == "2c6b3de0-86c2-4684-b576-4cfd4f50d6ad"
    assert cuboid.name == "lidar__cuboid__person"
    assert cuboid.pos == point3d
    assert cuboid.quat == quaternion
    assert cuboid.size == size3d
    assert cuboid.object == object_person
    assert cuboid.sensor == sensor_lidar
    assert cuboid.attributes == attributes_multiple_types


def test_asdict(
    point3d, point3d_dict,
    size3d, size3d_dict,
    quaternion, quaternion_dict,
    sensor_lidar,
    object_person,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    cuboid = Cuboid(
        uid="2c6b3de0-86c2-4684-b576-4cfd4f50d6ad",
        pos=point3d,
        quat=quaternion,
        size=size3d,
        object=object_person,
        sensor=sensor_lidar,
        attributes=attributes_multiple_types,
    )

    assert cuboid.asdict() == {
        "uid": "2c6b3de0-86c2-4684-b576-4cfd4f50d6ad",
        "name": "lidar__cuboid__person",
        "val": point3d_dict + quaternion_dict + size3d_dict,
        "coordinate_system": sensor_lidar.uid,
        "attributes": attributes_multiple_types_dict
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
