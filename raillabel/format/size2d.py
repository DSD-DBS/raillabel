# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Size2d:
    """The size of a rectangle in a 2d image."""

    x: int | float
    "The size along the x-axis."

    y: int | float
    "The size along the y-axis."

    @classmethod
    def from_json(cls, json: tuple[int | float, int | float]) -> Size2d:
        """Construct an instant of this class from RailLabel JSON data."""
        return Size2d(x=json[0], y=json[1])

    @classmethod
    def fromdict(cls, data_dict: dict) -> Size2d:
        """Generate a Size2d object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.

        """
        return Size2d(
            x=data_dict[0],
            y=data_dict[1],
        )

    def asdict(self) -> list[float]:
        """Export self as a dict compatible with the OpenLABEL schema."""
        return [float(self.x), float(self.y)]
