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
        uid="78f0ad89-2750-4a30-9d66-44c9da73a714",
        name="rgb_middle__seg3d__person",
        val=[1234, 5678],
        coordinate_system="lidar",
        attributes=attributes_multiple_types_json,
    )


@pytest.fixture
def seg3d(
    attributes_multiple_types,
) -> Seg3d:
    return Seg3d(
        point_ids=[1234, 5678],
        sensor="lidar",
        attributes=attributes_multiple_types,
        object=UUID("b40ba3ad-0327-46ff-9c28-2506cfd6d934"),
    )


# == Tests ============================


def test_from_json(seg3d, seg3d_json):
    actual = Seg3d.from_json(seg3d_json, object_uid=UUID("b40ba3ad-0327-46ff-9c28-2506cfd6d934"))
    assert actual == seg3d


# def test_name(seg3d):
#     actual = seg3d.name("person")
#     assert actual == "rgb_middle__seg3d__person"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
