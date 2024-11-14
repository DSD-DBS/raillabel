# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from ._json_format_base import _JSONFormatBase


class JSONStreamOther(_JSONFormatBase):
    """A stream describes the source of a data sequence, usually a sensor.

    This specific object describes a sensor without intrinsic calibration.
    """

    type: Literal["lidar", "gps_imu", "other"]
    "A string encoding the type of the stream."

    uri: str | None = None
    "A string encoding the subdirectory containing the sensor files."

    description: str | None = None
    "Description of the stream."
