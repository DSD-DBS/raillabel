# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from raillabel.json_format import JSONBbox

from ._attributes import _attributes_from_json, _attributes_to_json
from .point2d import Point2d
from .size2d import Size2d


@dataclass
class Bbox:
    """A 2D bounding box in an image."""

    pos: Point2d
    "The center point of the bbox in pixels."

    size: Size2d
    "The dimensions of the bbox in pixels from the top left corner to the bottom right corner."

    object: UUID
    "The uid of the object, this annotation belongs to."

    sensor: str
    "The uid of the sensor, this annotation is labeled in."

    attributes: dict[str, float | bool | str | list]
    "Additional information associated with the annotation."

    @classmethod
    def from_json(cls, json: JSONBbox, object_uid: UUID) -> Bbox:
        """Construct an instant of this class from RailLabel JSON data."""
        return Bbox(
            pos=Point2d.from_json((json.val[0], json.val[1])),
            size=Size2d.from_json((json.val[2], json.val[3])),
            object=object_uid,
            sensor=json.coordinate_system,
            attributes=_attributes_from_json(json.attributes),
        )

    def to_json(self, uid: UUID, object_type: str) -> JSONBbox:
        """Export this object into the RailLabel JSON format."""
        return JSONBbox(
            name=self.name(object_type),
            val=list(self.pos.to_json()) + list(self.size.to_json()),
            coordinate_system=self.sensor,
            uid=uid,
            attributes=_attributes_to_json(self.attributes),
        )

    def name(self, object_type: str) -> str:
        """Return the name of the annotation used for indexing in the object data pointers."""
        return f"{self.sensor}__bbox__{object_type}"
