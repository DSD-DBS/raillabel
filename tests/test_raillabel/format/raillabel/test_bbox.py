# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel._util._warning import _WarningsLogger
from raillabel.format import Bbox

# == Fixtures =========================

@pytest.fixture
def bbox_dict(
    sensor_camera,
    attributes_multiple_types_dict,
    point2d_dict,
    size2d_dict,
) -> dict:
    return {
        "uid": "78f0ad89-2750-4a30-9d66-44c9da73a714",
        "name": "rgb_middle__bbox__person",
        "val": point2d_dict + size2d_dict,
        "coordinate_system": sensor_camera.uid,
        "attributes": attributes_multiple_types_dict
    }

@pytest.fixture
def bbox(
    point2d,
    size2d,
    sensor_camera,
    attributes_multiple_types,
    object_person,
) -> dict:
    return Bbox(
        uid="78f0ad89-2750-4a30-9d66-44c9da73a714",
        pos=point2d,
        size=size2d,
        sensor=sensor_camera,
        attributes=attributes_multiple_types,
        object=object_person,
    )


@pytest.fixture
def bbox_train_dict(sensor_camera, attributes_single_type_dict, point2d_dict, size2d_dict) -> dict:
    return {
        "uid": "6a7cfdb7-149d-4987-98dd-79d05a8cc8e6",
        "name": "rgb_middle__bbox__train",
        "val": point2d_dict + size2d_dict,
        "coordinate_system": sensor_camera.uid,
        "attributes": attributes_single_type_dict
    }

@pytest.fixture
def bbox_train(
    point2d,
    size2d,
    sensor_camera,
    attributes_single_type,
    object_train,
) -> dict:
    return Bbox(
        uid="6a7cfdb7-149d-4987-98dd-79d05a8cc8e6",
        pos=point2d,
        size=size2d,
        sensor=sensor_camera,
        attributes=attributes_single_type,
        object=object_train,
    )

# == Tests ============================

def test_fromdict(
    point2d, point2d_dict,
    size2d, size2d_dict,
    sensor_camera, sensors,
    object_person,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    bbox = Bbox.fromdict(
        {
            "uid": "78f0ad89-2750-4a30-9d66-44c9da73a714",
            "name": "rgb_middle__bbox__person",
            "val": point2d_dict + size2d_dict,
            "coordinate_system": sensor_camera.uid,
            "attributes": attributes_multiple_types_dict
        },
        sensors,
        object_person
    )

    assert bbox.uid == "78f0ad89-2750-4a30-9d66-44c9da73a714"
    assert bbox.name == "rgb_middle__bbox__person"
    assert bbox.pos == point2d
    assert bbox.size == size2d
    assert bbox.object == object_person
    assert bbox.sensor == sensor_camera
    assert bbox.attributes == attributes_multiple_types

def test_fromdict_unknown_coordinate_system_warning(
    point2d_dict,
    size2d_dict,
    sensors,
    object_person,
):
    with _WarningsLogger() as logger:
        bbox = Bbox.fromdict(
            {
                "uid": "78f0ad89-2750-4a30-9d66-44c9da73a714",
                "name": "rgb_middle__bbox__person",
                "val": point2d_dict + size2d_dict,
                "coordinate_system": "UNKNOWN_COORDINATE_SYSTEM",
            },
            sensors,
            object_person
        )

    assert len(logger.warnings) == 1
    assert "78f0ad89-2750-4a30-9d66-44c9da73a714" in logger.warnings[0]
    assert "'UNKNOWN_COORDINATE_SYSTEM'" in logger.warnings[0]
    assert "sensor" in logger.warnings[0]

    assert bbox.sensor is None


def test_asdict(
    point2d, point2d_dict,
    size2d, size2d_dict,
    sensor_camera,
    object_person,
    attributes_multiple_types, attributes_multiple_types_dict,
):
    bbox = Bbox(
        uid="78f0ad89-2750-4a30-9d66-44c9da73a714",
        pos=point2d,
        size=size2d,
        object=object_person,
        sensor=sensor_camera,
        attributes=attributes_multiple_types,
    )

    assert bbox.asdict() == {
        "uid": "78f0ad89-2750-4a30-9d66-44c9da73a714",
        "name": "rgb_middle__bbox__person",
        "val": point2d_dict + size2d_dict,
        "coordinate_system": sensor_camera.uid,
        "attributes": attributes_multiple_types_dict
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
