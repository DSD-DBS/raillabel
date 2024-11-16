# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Radar, IntrinsicsRadar
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
            parent="base", type="sensor", pose_wrt_parent=transform_json, children=None
        ),
    )


@pytest.fixture
def radar(intrinsics_radar, transform) -> Radar:
    return Radar(
        intrinsics=intrinsics_radar,
        extrinsics=transform,
        uri="/path/to/sensor/data",
        description="A very nice radar",
    )


@pytest.fixture
def radar_empty() -> Radar:
    return Radar(
        intrinsics=IntrinsicsRadar(
            resolution_px_per_m=0,
            width_px=0,
            height_px=0,
        )
    )


# == Tests ============================


def test_from_json(radar, radar_json):
    actual = Radar.from_json(radar_json[0], radar_json[1])
    assert actual == radar


def test_to_json(radar, radar_json):
    actual = radar.to_json()
    assert actual == radar_json


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
