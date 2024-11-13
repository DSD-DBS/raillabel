# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from raillabel.json_format import JSONPoly2d

from ._attributes import _attributes_from_json
from .point2d import Point2d


@dataclass
class Poly2d:
    """Sequence of 2D points. Can either be a polygon or polyline."""

    points: list[Point2d]
    "List of the 2d points that make up the polyline."

    closed: bool
    "If True, this object represents a polygon and if False, it represents a polyline."

    object_id: UUID
    "The uid of the object, this annotation belongs to."

    sensor: str
    "The uid of the sensor, this annotation is labeled in."

    attributes: dict[str, float | bool | str | list]
    "Additional information associated with the annotation."

    @classmethod
    def from_json(cls, json: JSONPoly2d, object_id: UUID) -> Poly2d:
        """Construct an instant of this class from RailLabel JSON data."""
        return Poly2d(
            points=[
                Point2d(x=float(json.val[i]), y=float(json.val[i + 1]))
                for i in range(0, len(json.val), 2)
            ],
            closed=json.closed,
            object_id=object_id,
            sensor=json.coordinate_system,
            attributes=_attributes_from_json(json.attributes),
        )

    def name(self, object_type: str) -> str:
        """Return the name of the annotation used for indexing in the object data pointers."""
        return f"{self.sensor}__poly2d__{object_type}"
