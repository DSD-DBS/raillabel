# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

import pytest

from raillabel.format import Seg3d
from raillabel.json_format import JSONVec

# == Fixtures =========================


@pytest.fixture
def seg3d_json(
    attributes_multiple_types_json,
) -> JSONVec:
    return JSONVec(
        uid="d52e2b25-0B48-4899-86d5-4bc41be6b7d3",
        name="lidar__vec__person",
        val=[1234, 5678],
        coordinate_system="lidar",
        attributes=attributes_multiple_types_json,
    )


@pytest.fixture
def seg3d_id() -> UUID:
    return UUID("d52e2b25-0B48-4899-86d5-4bc41be6b7d3")


@pytest.fixture
def seg3d(
    attributes_multiple_types,
    object_person_id,
) -> Seg3d:
    return Seg3d(
        point_ids=[1234, 5678],
        sensor_id="lidar",
        attributes=attributes_multiple_types,
        object_id=object_person_id,
    )


# == Tests ============================


def test_from_json(seg3d, seg3d_json, object_person_id):
    actual = Seg3d.from_json(seg3d_json, object_person_id)
    assert actual == seg3d


def test_name(seg3d):
    actual = seg3d.name("person")
    assert actual == "lidar__vec__person"


def test_to_json(seg3d, seg3d_json, seg3d_id):
    actual = seg3d.to_json(seg3d_id, object_type="person")
    assert actual == seg3d_json


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
