# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

import pytest

from raillabel.format import Poly3d
from raillabel.json_format import JSONPoly3d

# == Fixtures =========================


@pytest.fixture
def poly3d_json(
    point3d_json,
    another_point3d_json,
    attributes_multiple_types_json,
) -> JSONPoly3d:
    return JSONPoly3d(
        uid="78f0ad89-2750-4a30-9d66-44c9da73a714",
        name="lidar__poly3d__person",
        closed=True,
        val=point3d_json + another_point3d_json,
        coordinate_system="lidar",
        attributes=attributes_multiple_types_json,
    )


@pytest.fixture
def poly3d(
    point3d,
    another_point3d,
    attributes_multiple_types,
) -> Poly3d:
    return Poly3d(
        points=[point3d, another_point3d],
        closed=True,
        sensor="lidar",
        attributes=attributes_multiple_types,
        object=UUID("b40ba3ad-0327-46ff-9c28-2506cfd6d934"),
    )


# == Tests ============================


def test_from_json(poly3d, poly3d_json):
    actual = Poly3d.from_json(poly3d_json, object_uid=UUID("b40ba3ad-0327-46ff-9c28-2506cfd6d934"))
    assert actual == poly3d


# def test_name(poly3d):
#     actual = poly3d.name("person")
#     assert actual == "lidar__poly3d__person"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
