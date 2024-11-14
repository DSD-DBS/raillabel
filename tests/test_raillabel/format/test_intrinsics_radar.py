# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import IntrinsicsRadar
from raillabel.json_format import JSONIntrinsicsRadar

# == Fixtures =========================


@pytest.fixture
def intrinsics_radar_json() -> dict:
    return JSONIntrinsicsRadar(
        resolution_px_per_m=2.856,
        width_px=2856,
        height_px=1428,
    )


@pytest.fixture
def intrinsics_radar() -> dict:
    return IntrinsicsRadar(
        resolution_px_per_m=2.856,
        width_px=2856,
        height_px=1428,
    )


# == Tests ============================


def test_from_json(intrinsics_radar, intrinsics_radar_json):
    actual = IntrinsicsRadar.from_json(intrinsics_radar_json)
    assert actual == intrinsics_radar


def test_to_json(intrinsics_radar, intrinsics_radar_json):
    actual = intrinsics_radar.to_json()
    assert actual == intrinsics_radar_json


if __name__ == "__main__":
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
