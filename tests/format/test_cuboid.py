# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

import pytest

from raillabel.format import Cuboid
from raillabel.json_format import JSONCuboid

# == Fixtures =========================


@pytest.fixture
def cuboid_json(
    attributes_multiple_types_json,
    point3d_json,
    quaternion_json,
    size3d_json,
) -> JSONCuboid:
    return JSONCuboid(
        uid="51def938-20BA-4699-95be-d6330c44cb77",
        name="lidar__cuboid__person",
        val=point3d_json + quaternion_json + size3d_json,
        coordinate_system="lidar",
        attributes=attributes_multiple_types_json,
    )


@pytest.fixture
def cuboid_id() -> UUID:
    return UUID("51def938-20BA-4699-95be-d6330c44cb77")


@pytest.fixture
def cuboid(
    point3d,
    size3d,
    quaternion,
    attributes_multiple_types,
    object_person_id,
) -> Cuboid:
    return Cuboid(
        pos=point3d,
        quat=quaternion,
        size=size3d,
        sensor_id="lidar",
        attributes=attributes_multiple_types,
        object_id=object_person_id,
    )


# == Tests ============================


def test_from_json(cuboid, cuboid_json, object_person_id):
    actual = Cuboid.from_json(cuboid_json, object_person_id)
    assert actual == cuboid


def test_name(cuboid):
    actual = cuboid.name("person")
    assert actual == "lidar__cuboid__person"


def test_to_json(cuboid, cuboid_json, cuboid_id):
    actual = cuboid.to_json(cuboid_id, object_type="person")
    assert actual == cuboid_json


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
