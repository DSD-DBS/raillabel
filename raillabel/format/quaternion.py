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

    @classmethod
    def fromdict(cls, data_dict: dict) -> Quaternion:
        """Generate a Quaternion object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.

        """
        return Quaternion(
            x=data_dict[0],
            y=data_dict[1],
            z=data_dict[2],
            w=data_dict[3],
        )

    def asdict(self) -> list[float]:
        """Export self as a dict compatible with the OpenLABEL schema."""
        return [float(self.x), float(self.y), float(self.z), float(self.w)]
