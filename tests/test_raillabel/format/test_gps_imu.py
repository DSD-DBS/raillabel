# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import GpsImu
from raillabel.json_format import JSONCoordinateSystem, JSONStreamOther

# == Fixtures =========================


@pytest.fixture
def gps_imu_json(transform_json) -> tuple[JSONStreamOther, JSONCoordinateSystem]:
    return (
        JSONStreamOther(
            type="gps_imu",
            uri="/path/to/sensor/data",
            description="A very nice gps_imu",
        ),
        JSONCoordinateSystem(
            parent="base", type="sensor", pose_wrt_parent=transform_json, children=None
        ),
    )


@pytest.fixture
def gps_imu(transform) -> dict:
    return GpsImu(
        extrinsics=transform,
        uri="/path/to/sensor/data",
        description="A very nice gps_imu",
    )


# == Tests ============================


def test_from_json(gps_imu, gps_imu_json):
    actual = GpsImu.from_json(gps_imu_json[0], gps_imu_json[1])
    assert actual == gps_imu


def test_to_json(gps_imu, gps_imu_json):
    actual = gps_imu.to_json()
    assert actual == gps_imu_json


if __name__ == "__main__":
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
