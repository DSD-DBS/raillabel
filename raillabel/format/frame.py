# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from raillabel.json_format import JSONFrame, JSONFrameProperties, JSONObjectData

from .bbox import Bbox
from .cuboid import Cuboid
from .num import Num
from .poly2d import Poly2d
from .poly3d import Poly3d
from .seg3d import Seg3d
from .sensor_reference import SensorReference


@dataclass
class Frame:
    """A container of dynamic, timewise, information."""

    timestamp: Decimal | None = None
    "Timestamp containing the Unix epoch time of the frame with up to nanosecond precision."

    sensors: dict[str, SensorReference] = field(default_factory=dict)
    "References to the sensors with frame specific information like timestamp and uri."

    frame_data: dict[str, Num] = field(default_factory=dict)
    """Dictionary containing data directly connected to the frame and not to any object, like
    gps/imu data. Dictionary keys are the ID-strings of the variable the data belongs to."""

    annotations: dict[UUID, Bbox | Cuboid | Poly2d | Poly3d | Seg3d] = field(default_factory=dict)
    "All annotations of this frame."

    @classmethod
    def from_json(cls, json: JSONFrame) -> Frame:
        """Construct an instant of this class from RailLabel JSON data."""
        return Frame(
            timestamp=_timestamp_from_dict(json.frame_properties),
            sensors=_sensors_from_dict(json.frame_properties),
            frame_data=_frame_data_from_dict(json.frame_properties),
            annotations=_annotations_from_json(json.objects),
        )


def _timestamp_from_dict(frame_properties: JSONFrameProperties | None) -> Decimal | None:
    if frame_properties is None:
        return None

    if frame_properties.timestamp is None:
        return None

    return Decimal(frame_properties.timestamp)


def _sensors_from_dict(frame_properties: JSONFrameProperties | None) -> dict[str, SensorReference]:
    if frame_properties is None:
        return {}

    if frame_properties.streams is None:
        return {}

    return {
        sensor_id: SensorReference.from_json(sensor_ref)
        for sensor_id, sensor_ref in frame_properties.streams.items()
    }


def _frame_data_from_dict(frame_properties: JSONFrameProperties | None) -> dict[str, Num]:
    if frame_properties is None:
        return {}

    if frame_properties.frame_data is None:
        return {}

    if frame_properties.frame_data.num is None:
        return {}

    return {num.name: Num.from_json(num) for num in frame_properties.frame_data.num}


def _annotations_from_json(
    json_object_data: dict[UUID, JSONObjectData] | None,
) -> dict[UUID, Bbox | Cuboid | Poly2d | Poly3d | Seg3d]:
    if json_object_data is None:
        return {}

    annotations: dict[UUID, Bbox | Cuboid | Poly2d | Poly3d | Seg3d] = {}

    for object_id, object_data in json_object_data.items():
        for json_bbox in _resolve_none_to_empty_list(object_data.object_data.bbox):
            annotations[json_bbox.uid] = Bbox.from_json(json_bbox, object_id)

        for json_cuboid in _resolve_none_to_empty_list(object_data.object_data.cuboid):
            annotations[json_cuboid.uid] = Cuboid.from_json(json_cuboid, object_id)

        for json_poly2d in _resolve_none_to_empty_list(object_data.object_data.poly2d):
            annotations[json_poly2d.uid] = Poly2d.from_json(json_poly2d, object_id)

        for json_poly3d in _resolve_none_to_empty_list(object_data.object_data.poly3d):
            annotations[json_poly3d.uid] = Poly3d.from_json(json_poly3d, object_id)

        for json_seg3d in _resolve_none_to_empty_list(object_data.object_data.vec):
            annotations[json_seg3d.uid] = Seg3d.from_json(json_seg3d, object_id)

    return annotations


def _resolve_none_to_empty_list(optional_list: list | None) -> list:
    if optional_list is None:
        return []
    return optional_list
