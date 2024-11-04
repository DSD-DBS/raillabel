# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point2d:
    """A 2d point in an image."""

    x: int | float
    "The x-coordinate of the point in the image in pixels."

    y: int | float
    "The y-coordinate of the point in the image in pixels."

    @classmethod
    def from_json(cls, json: tuple[int | float, int | float]) -> Point2d:
        """Construct an instant of this class from RailLabel JSON data."""
        return Point2d(x=json[0], y=json[1])

    @classmethod
    def fromdict(cls, data_dict: dict) -> Point2d:
        """Generate a Point2d object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.

        """
        return Point2d(
            x=data_dict[0],
            y=data_dict[1],
        )

    def asdict(self) -> list[float]:
        """Export self as a dict compatible with the OpenLABEL schema."""
        return [float(self.x), float(self.y)]
