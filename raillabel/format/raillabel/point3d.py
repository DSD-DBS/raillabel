# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Point3d:
    """A point in the 3D space.

    Parameters
    ----------
    x: float or int
        The x-coordinate of the point.
    y: float or int
        The y-coordinate of the point.
    z: float or int
        The z-coordinate of the point.
    """

    x: float
    y: float
    z: float

    @classmethod
    def fromdict(cls, data_dict: dict) -> "Point3d":
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

    def asdict(self) -> dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this class instance.

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.
        """

        return [float(self.x), float(self.y), float(self.z)]
