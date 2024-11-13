# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Size2d:
    """The size of a rectangle in a 2d image."""

    x: float
    "The size along the x-axis."

    y: float
    "The size along the y-axis."

    @classmethod
    def from_json(cls, json: tuple[float, float]) -> Size2d:
        """Construct an instant of this class from RailLabel JSON data."""
        return Size2d(x=json[0], y=json[1])

    def to_json(self) -> tuple[float, float]:
        """Export this object into the RailLabel JSON format."""
        return (self.x, self.y)
