# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from raillabel.json_format import JSONPoly3d

from ._attributes import _attributes_from_json, _attributes_to_json
from ._util import _flatten_list
from .point3d import Point3d


@dataclass
class Poly3d:
    """Sequence of 3D points. Can either be a polygon or polyline."""

    points: list[Point3d]
    "List of the 3d points that make up the polyline."

    closed: bool
    "If True, this object represents a polygon and if False, it represents a polyline."

    object_id: UUID
    "The unique identifyer of the real-life object, this annotation belongs to."

    sensor_id: str
    "The unique identifyer of the sensor this annotation is labeled in."

    attributes: dict[str, float | bool | str | list]
    "Additional information associated with the annotation."

    @classmethod
    def from_json(cls, json: JSONPoly3d, object_id: UUID) -> Poly3d:
        """Construct an instant of this class from RailLabel JSON data."""
        return Poly3d(
            points=[
                Point3d(x=float(json.val[i]), y=float(json.val[i + 1]), z=float(json.val[i + 2]))
                for i in range(0, len(json.val), 3)
            ],
            closed=json.closed,
            object_id=object_id,
            sensor_id=json.coordinate_system,
            attributes=_attributes_from_json(json.attributes),
        )

    def to_json(self, uid: UUID, object_type: str) -> JSONPoly3d:
        """Export this object into the RailLabel JSON format."""
        return JSONPoly3d(
            name=self.name(object_type),
            val=_flatten_list([point.to_json() for point in self.points]),
            closed=self.closed,
            coordinate_system=self.sensor_id,
            uid=uid,
            attributes=_attributes_to_json(self.attributes),
        )

    def name(self, object_type: str) -> str:
        """Return the name of the annotation used for indexing in the object data pointers."""
        return f"{self.sensor_id}__poly3d__{object_type}"
