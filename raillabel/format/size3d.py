# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Size3d:
    """The 3D size of a cube."""

    x: float
    "The size along the x-axis."

    y: float
    "The size along the y-axis."

    z: float
    "The size along the z-axis."

    @classmethod
    def from_json(cls, json: tuple[float, float, float]) -> Size3d:
        """Construct an instant of this class from RailLabel JSON data."""
        return Size3d(x=json[0], y=json[1], z=json[2])

    def to_json(self) -> tuple[float, float, float]:
        """Export this object into the RailLabel JSON format."""
        return (self.x, self.y, self.z)
