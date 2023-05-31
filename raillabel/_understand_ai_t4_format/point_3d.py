# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Point3d:
    """Dimensional information of an object in 3d.

    Parameters
    ----------
    x: float
        Position of the object in the x-dimension.
    y: float
        Position of the object in the y-dimension.
    z: float
        Position of the object in the z-dimension.
    """

    x: float
    y: float
    z: float

    @classmethod
    def fromdict(cls, data_dict: dict) -> "Point3d":
        """Generate a Point3d from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        Point3d
            Converted 3d point.
        """

        return Point3d(
            x=float(data_dict["x"]),
            y=float(data_dict["y"]),
            z=float(data_dict["z"]),
        )
