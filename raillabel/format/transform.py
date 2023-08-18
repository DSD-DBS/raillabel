# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass

from .point3d import Point3d
from .quaternion import Quaternion


@dataclass
class Transform:
    """A transformation between two coordinate systems.

    Parameters
    ----------
    pos: raillabel.format.Point3d
        Translation with regards to the parent coordinate system.
    quat: raillabel.format.Quaternion
        Rotation quaternion with regards to the parent coordinate system.
    """

    pos: Point3d
    quat: Quaternion

    @classmethod
    def fromdict(cls, data_dict: dict) -> "Transform":
        """Generate a Transform object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        """

        return Transform(
            pos=Point3d.fromdict(data_dict["translation"]),
            quat=Quaternion.fromdict(data_dict["quaternion"]),
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

        dict_repr = {
            "translation": self.pos.asdict(),
            "quaternion": self.quat.asdict(),
        }

        return dict_repr
