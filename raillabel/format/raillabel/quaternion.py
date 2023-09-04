# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Quaternion:
    """A quaternion.

    Parameters
    ----------
    x: float or int
        The x component of the quaternion.
    y: float or int
        The y component of the quaternion.
    z: float or int
        The z component of the quaternion.
    w: float or int
        The w component of the quaternion.
    """

    x: float
    y: float
    z: float
    w: float

    @classmethod
    def fromdict(cls, data_dict: dict) -> "Quaternion":
        """Generate a Quaternion object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        """

        return Quaternion(
            x=data_dict[0],
            y=data_dict[1],
            z=data_dict[2],
            w=data_dict[3],
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

        return [float(self.x), float(self.y), float(self.z), float(self.w)]
