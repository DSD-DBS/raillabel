# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Size3d:
    """The 3D size of a cube.

    Parameters
    ----------
    x: float or int
        The size along the x-axis.
    y: float or int
        The size along the y-axis.
    z: float or int
        The size along the z-axis.

    """

    x: float
    y: float
    z: float

    @classmethod
    def fromdict(cls, data_dict: dict) -> Size3d:
        """Generate a Size3d object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.

        """
        return Size3d(
            x=data_dict[0],
            y=data_dict[1],
            z=data_dict[2],
        )

    def asdict(self) -> list[float]:
        """Export self as a dict compatible with the OpenLABEL schema."""
        return [float(self.x), float(self.y), float(self.z)]
