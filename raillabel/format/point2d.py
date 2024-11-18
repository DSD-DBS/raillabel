# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point2d:
    """A 2d point in an image."""

    x: float
    "The x-coordinate of the point in the image in pixels from the left."

    y: float
    "The y-coordinate of the point in the image in pixels from the top."

    @classmethod
    def from_json(cls, json: tuple[float, float]) -> Point2d:
        """Construct an instant of this class from RailLabel JSON data."""
        return Point2d(x=json[0], y=json[1])

    def to_json(self) -> tuple[float, float]:
        """Export this object into the RailLabel JSON format."""
        return (self.x, self.y)
