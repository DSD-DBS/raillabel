# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Poly2d

# == Fixtures =========================

@pytest.fixture
def poly2d_dict(
    sensor_camera,
    attributes_multiple_types_dict,
    point2d_dict, point2d_another_dict
) -> dict:
    return {
        "uid": "d73b5988-767B-47ef-979c-022af60c6ab2",
        "name": "rgb_middle__poly2d__person",
        "val": point2d_dict + point2d_another_dict,
        "coordinate_system": sensor_camera.uid,
        "attributes": attributes_multiple_types_dict,
        "closed": True,
        "mode": "MODE_POLY2D_ABSOLUTE",
    }

@pytest.fixture
def poly2d(
    point2d, point2d_another,
    sensor_camera,
    attributes_multiple_types,
    object_person
) -> dict:
    return Poly2d(
        uid="d73b5988-767B-47ef-979c-022af60c6ab2",
        points=[point2d, point2d_another],
        object=object_person,
        sensor=sensor_camera,
        attributes=attributes_multiple_types,
        closed=True,
        mode="MODE_POLY2D_ABSOLUTE",
    )

# == Tests ============================

def test_fromdict(
    point2d, point2d_dict,
    point2d_another, point2d_another_dict,
    sensor_camera, sensors,
    object_person,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    poly2d = Poly2d.fromdict(
        {
            "uid": "d73b5988-767B-47ef-979c-022af60c6ab2",
            "name": "rgb_middle__poly2d__person",
            "val": point2d_dict + point2d_another_dict,
            "coordinate_system": sensor_camera.uid,
            "attributes": attributes_multiple_types_dict,
            "closed": True,
            "mode": "MODE_POLY2D_ABSOLUTE",
        },
        sensors,
        object_person
    )

    assert poly2d.uid == "d73b5988-767B-47ef-979c-022af60c6ab2"
    assert poly2d.name == "rgb_middle__poly2d__person"
    assert poly2d.points == [point2d, point2d_another]
    assert poly2d.object == object_person
    assert poly2d.sensor == sensor_camera
    assert poly2d.attributes == attributes_multiple_types
    assert poly2d.closed == True
    assert poly2d.mode == "MODE_POLY2D_ABSOLUTE"


def test_asdict(
    point2d, point2d_dict,
    point2d_another, point2d_another_dict,
    sensor_camera, object_person,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    poly2d = Poly2d(
        uid="d73b5988-767B-47ef-979c-022af60c6ab2",
        points=[point2d, point2d_another],
        object=object_person,
        sensor=sensor_camera,
        attributes=attributes_multiple_types,
        closed=True,
        mode="MODE_POLY2D_ABSOLUTE",
    )

    assert poly2d.asdict() == {
        "uid": "d73b5988-767B-47ef-979c-022af60c6ab2",
        "name": "rgb_middle__poly2d__person",
        "val": point2d_dict + point2d_another_dict,
        "coordinate_system": sensor_camera.uid,
        "attributes": attributes_multiple_types_dict,
        "closed": True,
        "mode": "MODE_POLY2D_ABSOLUTE",
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
