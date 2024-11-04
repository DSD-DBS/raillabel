# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class JSONStreamRadar(BaseModel):
    """A stream describes the source of a data sequence, usually a sensor.

    This specific object contains the intrinsics of a radar sensor.
    """

    type: Literal["radar"]
    "A string encoding the type of the stream."

    stream_properties: JSONStreamRadarProperties
    "Intrinsic calibration of the stream."

    uri: str
    "A string encoding the subdirectory containing the sensor files."

    description: str | None = None
    "Description of the stream."


class JSONStreamRadarProperties(BaseModel):
    """Intrinsic calibration of the stream."""

    intrinsics_radar: JSONIntrinsicsRadar


class JSONIntrinsicsRadar(BaseModel):
    """JSON object defining an instance of the intrinsic parameters of a radar."""

    resolution_px_per_m: float
    "Number correlating pixel in the output image to a position relative to the sensor in meters."

    height_px: int
    "Height of the radar output in pixel."

    width_px: int
    "Width of the radar output in pixel."
