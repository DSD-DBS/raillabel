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

    pos: Point3d
    "Translation with regards to the parent coordinate system."

    quat: Quaternion
    "Rotation quaternion with regards to the parent coordinate system."

    @classmethod
    def from_json(cls, json: JSONTransformData) -> Transform:
        """Construct an instant of this class from RailLabel JSON data."""
        return Transform(
            pos=Point3d.from_json(json.translation),
            quat=Quaternion.from_json(json.quaternion),
        )

    def to_json(self) -> JSONTransformData:
        """Export this object into the RailLabel JSON format."""
        return JSONTransformData(
            translation=self.pos.to_json(),
            quaternion=self.quat.to_json(),
        )
