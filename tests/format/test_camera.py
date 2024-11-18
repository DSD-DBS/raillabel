# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Camera, IntrinsicsPinhole
from raillabel.json_format import (
    JSONCoordinateSystem,
    JSONStreamCamera,
    JSONStreamCameraProperties,
    JSONIntrinsicsPinhole,
)

# == Fixtures =========================


@pytest.fixture
def camera_json(
    intrinsics_pinhole_json, transform_json
) -> tuple[JSONStreamCamera, JSONCoordinateSystem]:
    return (
        JSONStreamCamera(
            type="camera",
            stream_properties=JSONStreamCameraProperties(intrinsics_pinhole=intrinsics_pinhole_json),
            uri="/path/to/sensor/data",
            description="A very nice camera",
        ),
        JSONCoordinateSystem(
            parent="base", type="sensor", pose_wrt_parent=transform_json, children=None
        ),
    )


@pytest.fixture
def camera(intrinsics_pinhole, transform) -> Camera:
    return Camera(
        intrinsics=intrinsics_pinhole,
        extrinsics=transform,
        uri="/path/to/sensor/data",
        description="A very nice camera",
    )


@pytest.fixture
def camera_empty() -> Camera:
    return Camera(
        intrinsics=IntrinsicsPinhole(
            camera_matrix=tuple([0] * 12),
            distortion=tuple([0] * 5),
            width_px=0,
            height_px=0,
        )
    )


# == Tests ============================


def test_from_json(camera, camera_json):
    actual = Camera.from_json(camera_json[0], camera_json[1])
    assert actual == camera


def test_to_json(camera, camera_json):
    actual = camera.to_json()
    assert actual == camera_json


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
