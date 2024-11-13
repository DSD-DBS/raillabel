# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point3d:
    """A point in the 3D space."""

    x: float
    "The x-coordinate of the point."

    y: float
    "The y-coordinate of the point."

    z: float
    "The z-coordinate of the point."

    @classmethod
    def from_json(cls, json: tuple[float, float, float]) -> Point3d:
        """Construct an instant of this class from RailLabel JSON data."""
        return Point3d(x=json[0], y=json[1], z=json[2])

    def to_json(self) -> tuple[float, float, float]:
        """Export this object into the RailLabel JSON format."""
        return (self.x, self.y, self.z)
