# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class JSONStreamRadar(BaseModel):
    """A stream describes the source of a data sequence, usually a sensor.

    This specific object describes a sensor without intrinsic calibration.
    """

    type: Literal["lidar", "gps_imu", "other"]
    "A string encoding the type of the stream."

    uri: str | None
    "A string encoding the subdirectory containing the sensor files."

    description: str | None
    "Description of the stream."
