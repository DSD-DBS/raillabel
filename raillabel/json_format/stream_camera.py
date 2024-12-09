# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from ._json_format_base import _JSONFormatBase


class JSONStreamCamera(_JSONFormatBase):
    """A stream describes the source of a data sequence, usually a sensor.

    This specific object contains the intrinsics of a camera sensor.
    """

    type: Literal["camera"]
    "A string encoding the type of the stream."

    stream_properties: JSONStreamCameraProperties
    "Intrinsic calibration of the stream."

    uri: str | None = None
    "A string encoding the subdirectory containing the sensor files."

    description: str | None = None
    "Description of the stream."


class JSONStreamCameraProperties(_JSONFormatBase):
    """Intrinsic calibration of the stream."""

    intrinsics_pinhole: JSONIntrinsicsPinhole


class JSONIntrinsicsPinhole(_JSONFormatBase):
    """JSON object defining an instance of the intrinsic parameters of a pinhole camera."""

    camera_matrix: tuple[
        float, float, float, float, float, float, float, float, float, float, float, float
    ]
    """This is a 3x4 camera matrix which projects 3D homogeneous points (4x1) from a camera
    coordinate system into the image plane (3x1). This is the usual K matrix for camera projection as
    in OpenCV. It is extended from 3x3 to 3x4 to enable its direct utilisation to project 4x1
    homogeneous 3D points. The matrix is defined to follow the camera model: x-to-right, y-down,
    z-forward. The following equation applies: x_img = camera_matrix * X_ccs."""

    distortion_coeffs: tuple[float, float, float, float, float]
    "This is the array 1x5 radial and tangential distortion coefficients."

    height_px: int
    "Height of the camera output in pixel."

    width_px: int
    "Width of the camera output in pixel."
