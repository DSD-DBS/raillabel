# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Poly3d

# == Fixtures =========================

@pytest.fixture
def poly3d_dict(
    sensor_lidar,
    attributes_multiple_types_dict,
    point3d_dict, point3d_another_dict
) -> dict:
    return {
        "uid": "9a9a30f5-D334-4f11-aa3f-c3c83f2935eb",
        "name": "lidar__poly3d__person",
        "val": point3d_dict + point3d_another_dict,
        "coordinate_system": sensor_lidar.uid,
        "attributes": attributes_multiple_types_dict,
        "closed": True,
    }

@pytest.fixture
def poly3d(
    point3d, point3d_another,
    sensor_lidar,
    object_person,
    attributes_multiple_types
) -> dict:
    return Poly3d(
        uid="9a9a30f5-D334-4f11-aa3f-c3c83f2935eb",
        points=[point3d, point3d_another],
        object=object_person,
        sensor=sensor_lidar,
        attributes=attributes_multiple_types,
        closed=True,
    )

# == Tests ============================

def test_fromdict(
    point3d, point3d_dict,
    point3d_another, point3d_another_dict,
    sensor_lidar, sensors,
    object_person,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    poly3d = Poly3d.fromdict(
        {
            "uid": "9a9a30f5-D334-4f11-aa3f-c3c83f2935eb",
            "name": "lidar__poly3d__person",
            "val": point3d_dict + point3d_another_dict,
            "coordinate_system": sensor_lidar.uid,
            "attributes": attributes_multiple_types_dict,
            "closed": True,
        },
        sensors,
        object_person
    )

    assert poly3d.uid == "9a9a30f5-D334-4f11-aa3f-c3c83f2935eb"
    assert poly3d.name == "lidar__poly3d__person"
    assert poly3d.points == [point3d, point3d_another]
    assert poly3d.object == object_person
    assert poly3d.sensor == sensor_lidar
    assert poly3d.attributes == attributes_multiple_types
    assert poly3d.closed == True


def test_asdict(
    point3d, point3d_dict,
    point3d_another, point3d_another_dict,
    sensor_lidar,
    object_person,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    poly3d = Poly3d(
        uid="9a9a30f5-D334-4f11-aa3f-c3c83f2935eb",
        points=[point3d, point3d_another],
        object=object_person,
        sensor=sensor_lidar,
        attributes=attributes_multiple_types,
        closed=True,
    )

    assert poly3d.asdict() == {
        "uid": "9a9a30f5-D334-4f11-aa3f-c3c83f2935eb",
        "name": "lidar__poly3d__person",
        "val": point3d_dict + point3d_another_dict,
        "coordinate_system": sensor_lidar.uid,
        "attributes": attributes_multiple_types_dict,
        "closed": True,
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
