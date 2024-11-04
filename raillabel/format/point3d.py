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

    @classmethod
    def fromdict(cls, data_dict: dict) -> Point3d:
        """Generate a Point3d object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.

        """
        return Point3d(
            x=data_dict[0],
            y=data_dict[1],
            z=data_dict[2],
        )

    def asdict(self) -> list[float]:
        """Export self as a dict compatible with the OpenLABEL schema."""
        return [float(self.x), float(self.y), float(self.z)]
