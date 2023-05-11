# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Quaternion:
    """Dimensional information of an object in 3d.

    Parameters
    ----------
    x: float
        The x component of the quaternion.
    y: float
        The y component of the quaternion.
    z: float
        The z component of the quaternion.
    w: float
        The w component of the quaternion.
    """

    x: float
    y: float
    z: float
    w: float

    @classmethod
    def fromdict(cls, data_dict: dict) -> "Quaternion":
        """Generate a Quaternion from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        Quaternion
            Converted quaternion.
        """

        return Quaternion(
            x=float(data_dict["x"]),
            y=float(data_dict["y"]),
            z=float(data_dict["z"]),
            w=float(data_dict["w"]),
        )
