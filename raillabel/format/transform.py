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
            "translation": [self.pos.x, self.pos.y, self.pos.z],
            "quaternion": [self.quat.x, self.quat.y, self.quat.z, self.quat.w],
        }

        return dict_repr
