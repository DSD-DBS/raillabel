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
            position=Point3d.from_json(json.translation),
            quaternion=Quaternion.from_json(json.quaternion),
        )
