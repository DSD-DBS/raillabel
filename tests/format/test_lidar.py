# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Lidar
from raillabel.json_format import JSONCoordinateSystem, JSONStreamOther

# == Fixtures =========================


@pytest.fixture
def lidar_json(transform_json) -> tuple[JSONStreamOther, JSONCoordinateSystem]:
    return (
        JSONStreamOther(
            type="lidar",
            uri="/path/to/sensor/data",
            description="A very nice lidar",
        ),
        JSONCoordinateSystem(
            parent="base", type="sensor", pose_wrt_parent=transform_json, children=None
        ),
    )


@pytest.fixture
def lidar(transform) -> dict:
    return Lidar(
        extrinsics=transform,
        uri="/path/to/sensor/data",
        description="A very nice lidar",
    )


# == Tests ============================


def test_from_json(lidar, lidar_json):
    actual = Lidar.from_json(lidar_json[0], lidar_json[1])
    assert actual == lidar


def test_to_json(lidar, lidar_json):
    actual = lidar.to_json()
    assert actual == lidar_json


if __name__ == "__main__":
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
