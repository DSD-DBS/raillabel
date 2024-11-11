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
        uid="78f0ad89-2750-4a30-9d66-44c9da73a714",
        name="lidar__cuboid__person",
        val=point3d_json + quaternion_json + size3d_json,
        coordinate_system="lidar",
        attributes=attributes_multiple_types_json,
    )


@pytest.fixture
def cuboid(
    point3d,
    size3d,
    quaternion,
    attributes_multiple_types,
) -> Cuboid:
    return Cuboid(
        pos=point3d,
        quat=quaternion,
        size=size3d,
        sensor="lidar",
        attributes=attributes_multiple_types,
        object=UUID("b40ba3ad-0327-46ff-9c28-2506cfd6d934"),
    )


# == Tests ============================


def test_from_json(cuboid, cuboid_json):
    actual = Cuboid.from_json(cuboid_json, object_uid=UUID("b40ba3ad-0327-46ff-9c28-2506cfd6d934"))
    assert actual == cuboid


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
