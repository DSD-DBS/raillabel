# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from raillabel.json_format import JSONVec

from ._attributes import _attributes_from_json


@dataclass
class Seg3d:
    """The 3D segmentation of a lidar pointcloud."""

    point_ids: list[int]
    "The list of point indices."

    object_id: UUID
    "The unique identifyer of the real-life object, this annotation belongs to."

    sensor: str
    "The uid of the sensor, this annotation is labeled in."

    attributes: dict[str, float | bool | str | list]
    "Additional information associated with the annotation."

    @classmethod
    def from_json(cls, json: JSONVec, object_id: UUID) -> Seg3d:
        """Construct an instant of this class from RailLabel JSON data."""
        return Seg3d(
            point_ids=[int(point_id) for point_id in json.val],
            object_id=object_id,
            sensor=json.coordinate_system,
            attributes=_attributes_from_json(json.attributes),
        )

    def name(self, object_type: str) -> str:
        """Return the name of the annotation used for indexing in the object data pointers."""
        return f"{self.sensor}__vec__{object_type}"
