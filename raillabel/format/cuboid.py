# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from raillabel.json_format import JSONCuboid

from ._attributes import _attributes_from_json
from .point3d import Point3d
from .quaternion import Quaternion
from .size3d import Size3d


@dataclass
class Cuboid:
    """3D bounding box."""

    pos: Point3d
    """The center position of the cuboid in meters, where the x coordinate points ahead of the
    vehicle, y points to the left and z points upwards."""

    quat: Quaternion
    "The rotation of the cuboid in quaternions."

    size: Size3d
    "The size of the cuboid in meters."

    object: UUID
    "The uid of the object, this annotation belongs to."

    sensor: str
    "The uid of the sensor, this annotation is labeled in."

    attributes: dict[str, float | bool | str | list]
    "Additional information associated with the annotation."

    @classmethod
    def from_json(cls, json: JSONCuboid, object_uid: UUID) -> Cuboid:
        """Construct an instant of this class from RailLabel JSON data."""
        return Cuboid(
            pos=Point3d.from_json((json.val[0], json.val[1], json.val[2])),
            quat=Quaternion.from_json((json.val[3], json.val[4], json.val[5], json.val[6])),
            size=Size3d.from_json((json.val[7], json.val[8], json.val[9])),
            object=object_uid,
            sensor=json.coordinate_system,
            attributes=_attributes_from_json(json.attributes),
        )

    def name(self, object_type: str) -> str:
        """Return the name of the annotation used for indexing in the object data pointers."""
        return f"{self.sensor}__cuboid__{object_type}"
