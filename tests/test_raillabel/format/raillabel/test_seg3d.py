# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Seg3d

# == Fixtures =========================

@pytest.fixture
def seg3d_dict(sensor_lidar, attributes_multiple_types_dict) -> dict:
    return {
        "uid": "db4e4a77-B926-4a6c-a2a6-e0ecf9d8734a",
        "name": "lidar__vec__person",
        "val": [586, 789, 173],
        "coordinate_system": sensor_lidar.uid,
        "attributes": attributes_multiple_types_dict
    }

@pytest.fixture
def seg3d(sensor_lidar, attributes_multiple_types, object_person) -> dict:
    return Seg3d(
        uid="db4e4a77-B926-4a6c-a2a6-e0ecf9d8734a",
        point_ids=[586, 789, 173],
        object=object_person,
        sensor=sensor_lidar,
        attributes=attributes_multiple_types,
    )

# == Tests ============================

def test_fromdict(
    sensor_lidar, sensors,
    object_person,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    seg3d = Seg3d.fromdict(
        {
            "uid": "db4e4a77-B926-4a6c-a2a6-e0ecf9d8734a",
            "name": "lidar__vec__person",
            "val": [586, 789, 173],
            "coordinate_system": sensor_lidar.uid,
            "attributes": attributes_multiple_types_dict
        },
        sensors,
        object_person
    )

    assert seg3d.uid == "db4e4a77-B926-4a6c-a2a6-e0ecf9d8734a"
    assert seg3d.name == "lidar__vec__person"
    assert seg3d.point_ids == [586, 789, 173]
    assert seg3d.object == object_person
    assert seg3d.sensor == sensor_lidar
    assert seg3d.attributes == attributes_multiple_types


def test_asdict(
    sensor_lidar, sensors,
    object_person,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    seg3d = Seg3d(
        uid="db4e4a77-B926-4a6c-a2a6-e0ecf9d8734a",
        point_ids=[586, 789, 173],
        object=object_person,
        sensor=sensor_lidar,
        attributes=attributes_multiple_types,
    )

    assert seg3d.asdict() == {
        "uid": "db4e4a77-B926-4a6c-a2a6-e0ecf9d8734a",
        "name": "lidar__vec__person",
        "val": [586, 789, 173],
        "coordinate_system": sensor_lidar.uid,
        "attributes": attributes_multiple_types_dict
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
