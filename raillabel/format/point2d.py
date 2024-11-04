# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point2d:
    """A 2d point in an image."""

    x: int | float
    "The x-coordinate of the point in the image in pixels from the left."

    y: int | float
    "The y-coordinate of the point in the image in pixels from the top."

    @classmethod
    def from_json(cls, json: tuple[int | float, int | float]) -> Point2d:
        """Construct an instant of this class from RailLabel JSON data."""
        return Point2d(x=json[0], y=json[1])
