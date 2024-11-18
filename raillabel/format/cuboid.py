# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from raillabel.json_format import JSONCuboid

from ._attributes import _attributes_from_json, _attributes_to_json
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

    object_id: UUID
    "The unique identifyer of the real-life object, this annotation belongs to."

    sensor_id: str
    "The unique identifyer of the sensor this annotation is labeled in."

    attributes: dict[str, float | bool | str | list]
    "Additional information associated with the annotation."

    @classmethod
    def from_json(cls, json: JSONCuboid, object_id: UUID) -> Cuboid:
        """Construct an instant of this class from RailLabel JSON data."""
        return Cuboid(
            pos=Point3d.from_json((json.val[0], json.val[1], json.val[2])),
            quat=Quaternion.from_json((json.val[3], json.val[4], json.val[5], json.val[6])),
            size=Size3d.from_json((json.val[7], json.val[8], json.val[9])),
            object_id=object_id,
            sensor_id=json.coordinate_system,
            attributes=_attributes_from_json(json.attributes),
        )

    def to_json(self, uid: UUID, object_type: str) -> JSONCuboid:
        """Export this object into the RailLabel JSON format."""
        return JSONCuboid(
            name=self.name(object_type),
            val=list(self.pos.to_json()) + list(self.quat.to_json()) + list(self.size.to_json()),
            coordinate_system=self.sensor_id,
            uid=uid,
            attributes=_attributes_to_json(self.attributes),
        )

    def name(self, object_type: str) -> str:
        """Return the name of the annotation used for indexing in the object data pointers."""
        return f"{self.sensor_id}__cuboid__{object_type}"
