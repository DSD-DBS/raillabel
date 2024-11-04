# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.json_format import JSONTransformData

from .point3d import Point3d
from .quaternion import Quaternion


@dataclass
class Transform:
    """A transformation between two coordinate systems."""

    position: Point3d
    "Translation with regards to the parent coordinate system."

    quaternion: Quaternion
    "Rotation quaternion with regards to the parent coordinate system."

    @classmethod
    def from_json(cls, json: JSONTransformData) -> Transform:
        """Construct an instant of this class from RailLabel JSON data."""
        return Transform(
            position=Point3d(x=json.translation[0], y=json.translation[1], z=json.translation[2]),
            quaternion=Quaternion(
                x=json.quaternion[0],
                y=json.quaternion[1],
                z=json.quaternion[2],
                w=json.quaternion[3],
            ),
        )

    @classmethod
    def fromdict(cls, data_dict: dict) -> Transform:
        """Generate a Transform object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.

        """
        return Transform(
            position=Point3d.fromdict(data_dict["translation"]),
            quaternion=Quaternion.fromdict(data_dict["quaternion"]),
        )

    def asdict(self) -> dict[str, list[float]]:
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
        return {
            "translation": self.position.asdict(),
            "quaternion": self.quaternion.asdict(),
        }
