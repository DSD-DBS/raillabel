# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Quaternion:
    """A rotation represented by a quaternion."""

    x: float
    "The x component of the quaternion."

    y: float
    "The y component of the quaternion."

    z: float
    "The z component of the quaternion."

    w: float
    "The omega component of the quaternion."

    @classmethod
    def from_json(cls, json: tuple[float, float, float, float]) -> Quaternion:
        """Construct an instant of this class from RailLabel JSON data."""
        return Quaternion(x=json[0], y=json[1], z=json[2], w=json[3])

    def to_json(self) -> tuple[float, float, float, float]:
        """Export this object into the RailLabel JSON format."""
        return (self.x, self.y, self.z, self.w)
