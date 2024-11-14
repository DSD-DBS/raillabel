# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.json_format import JSONIntrinsicsRadar


@dataclass
class IntrinsicsRadar:
    """Intrinsic calibration for a radar sensor."""

    resolution_px_per_m: float
    """Factor for calculating the 3D coordinates of a pixel in the cartesian radar images. Number of
    pixels in the images per meter from the sensor."""

    width_px: int
    "Width of the cartesian image frame in pixel."

    height_px: int
    "Height of the cartesian image frame in pixel."

    @classmethod
    def from_json(cls, json: JSONIntrinsicsRadar) -> IntrinsicsRadar:
        """Construct an instant of this class from RailLabel JSON data."""
        return IntrinsicsRadar(
            resolution_px_per_m=json.resolution_px_per_m,
            width_px=json.width_px,
            height_px=json.height_px,
        )

    def to_json(self) -> JSONIntrinsicsRadar:
        """Export this object into the RailLabel JSON format."""
        return JSONIntrinsicsRadar(
            resolution_px_per_m=self.resolution_px_per_m,
            width_px=self.width_px,
            height_px=self.height_px,
        )
