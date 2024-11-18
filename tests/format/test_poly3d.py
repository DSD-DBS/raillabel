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
        uid="0da87210-46F1-40e5-b661-20ea1c392f50",
        name="lidar__poly3d__track",
        closed=True,
        val=point3d_json + another_point3d_json,
        coordinate_system="lidar",
        attributes=attributes_multiple_types_json,
    )


@pytest.fixture
def poly3d_id() -> UUID:
    return UUID("0da87210-46F1-40e5-b661-20ea1c392f50")


@pytest.fixture
def poly3d(
    point3d,
    another_point3d,
    attributes_multiple_types,
    object_track_id,
) -> Poly3d:
    return Poly3d(
        points=[point3d, another_point3d],
        closed=True,
        sensor_id="lidar",
        attributes=attributes_multiple_types,
        object_id=object_track_id,
    )


# == Tests ============================


def test_from_json(poly3d, poly3d_json, object_track_id):
    actual = Poly3d.from_json(poly3d_json, object_track_id)
    assert actual == poly3d


def test_name(poly3d):
    actual = poly3d.name("track")
    assert actual == "lidar__poly3d__track"


def test_to_json(poly3d, poly3d_json, poly3d_id):
    actual = poly3d.to_json(poly3d_id, object_type="track")
    assert actual == poly3d_json


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
