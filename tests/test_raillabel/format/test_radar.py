# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Radar
from raillabel.json_format import (
    JSONCoordinateSystem,
    JSONStreamRadar,
    JSONStreamRadarProperties,
    JSONIntrinsicsRadar,
)

# == Fixtures =========================


@pytest.fixture
def radar_json(
    intrinsics_radar_json, transform_json
) -> tuple[JSONStreamRadar, JSONCoordinateSystem]:
    return (
        JSONStreamRadar(
            type="radar",
            stream_properties=JSONStreamRadarProperties(intrinsics_radar=intrinsics_radar_json),
            uri="/path/to/sensor/data",
            description="A very nice radar",
        ),
        JSONCoordinateSystem(
            parent="base", type="sensor", pose_wrt_parent=transform_json, children=[]
        ),
    )


@pytest.fixture
def radar(intrinsics_radar, transform) -> dict:
    return Radar(
        intrinsics=intrinsics_radar,
        extrinsics=transform,
        uri="/path/to/sensor/data",
        description="A very nice radar",
    )


# == Tests ============================


def test_from_json(radar, radar_json):
    actual = Radar.from_json(radar_json[0], radar_json[1])
    assert actual == radar


if __name__ == "__main__":
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
