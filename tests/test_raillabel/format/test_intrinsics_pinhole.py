# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import IntrinsicsPinhole
from raillabel.json_format import JSONIntrinsicsPinhole

# == Fixtures =========================


@pytest.fixture
def intrinsics_pinhole_dict() -> dict:
    return {
        "camera_matrix": [0.48, 0, 0.81, 0, 0, 0.16, 0.83, 0, 0, 0, 1, 0],
        "distortion_coeffs": [0.49, 0.69, 0.31, 0.81, 0.99],
        "width_px": 2464,
        "height_px": 1600,
    }


@pytest.fixture
def intrinsics_pinhole_json() -> dict:
    return JSONIntrinsicsPinhole(
        camera_matrix=[0.48, 0, 0.81, 0, 0, 0.16, 0.83, 0, 0, 0, 1, 0],
        distortion_coeffs=[0.49, 0.69, 0.31, 0.81, 0.99],
        width_px=2464,
        height_px=1600,
    )


@pytest.fixture
def intrinsics_pinhole() -> dict:
    return IntrinsicsPinhole(
        camera_matrix=(0.48, 0, 0.81, 0, 0, 0.16, 0.83, 0, 0, 0, 1, 0),
        distortion=(0.49, 0.69, 0.31, 0.81, 0.99),
        width_px=2464,
        height_px=1600,
    )


# == Tests ============================


def test_from_json(intrinsics_pinhole, intrinsics_pinhole_json):
    actual = IntrinsicsPinhole.from_json(intrinsics_pinhole_json)
    assert actual == intrinsics_pinhole


def test_fromdict():
    intrinsics_pinhole = IntrinsicsPinhole.fromdict(
        {
            "camera_matrix": [0.48, 0, 0.81, 0, 0, 0.16, 0.83, 0, 0, 0, 1, 0],
            "distortion_coeffs": [0.49, 0.69, 0.31, 0.81, 0.99],
            "width_px": 2464,
            "height_px": 1600,
        }
    )

    assert intrinsics_pinhole.camera_matrix == (0.48, 0, 0.81, 0, 0, 0.16, 0.83, 0, 0, 0, 1, 0)
    assert intrinsics_pinhole.distortion == (0.49, 0.69, 0.31, 0.81, 0.99)
    assert intrinsics_pinhole.width_px == 2464
    assert intrinsics_pinhole.height_px == 1600


def test_asdict():
    intrinsics_pinhole = IntrinsicsPinhole(
        camera_matrix=(0.48, 0, 0.81, 0, 0, 0.16, 0.83, 0, 0, 0, 1, 0),
        distortion=(0.49, 0.69, 0.31, 0.81, 0.99),
        width_px=2464,
        height_px=1600,
    )

    assert intrinsics_pinhole.asdict() == {
        "camera_matrix": [0.48, 0, 0.81, 0, 0, 0.16, 0.83, 0, 0, 0, 1, 0],
        "distortion_coeffs": [0.49, 0.69, 0.31, 0.81, 0.99],
        "width_px": 2464,
        "height_px": 1600,
    }


if __name__ == "__main__":
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
