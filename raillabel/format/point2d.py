# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point2d:
    """A 2d point in an image.

    Parameters
    ----------
    x: float or int
        The x-coordinate of the point in the image.
    y: float or int
        The y-coordinate of the point in the image.

    """

    x: float
    y: float

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
