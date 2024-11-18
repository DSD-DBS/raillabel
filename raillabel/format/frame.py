# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from raillabel.json_format import (
    JSONAnnotations,
    JSONFrame,
    JSONFrameData,
    JSONFrameProperties,
    JSONObjectData,
)

from ._util import _empty_list_to_none
from .bbox import Bbox
from .cuboid import Cuboid
from .num import Num
from .object import Object
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

    def to_json(self, objects: dict[UUID, Object]) -> JSONFrame:
        """Export this object into the RailLabel JSON format."""
        return JSONFrame(
            frame_properties=JSONFrameProperties(
                timestamp=self.timestamp,
                streams={
                    sensor_id: sensor_ref.to_json() for sensor_id, sensor_ref in self.sensors.items()
                },
                frame_data=JSONFrameData(num=[num.to_json() for num in self.frame_data.values()]),
            ),
            objects=_objects_to_json(self.annotations, objects),
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


def _objects_to_json(
    annotations: dict[UUID, Bbox | Cuboid | Poly2d | Poly3d | Seg3d], objects: dict[UUID, Object]
) -> dict[str, JSONObjectData] | None:
    if len(annotations) == 0:
        return None

    object_data = {}

    for ann_id, annotation in annotations.items():
        object_id = str(annotation.object_id)

        if object_id not in object_data:
            object_data[object_id] = JSONObjectData(
                object_data=JSONAnnotations(
                    bbox=[],
                    cuboid=[],
                    poly2d=[],
                    poly3d=[],
                    vec=[],
                )
            )

        json_annotation = annotation.to_json(ann_id, objects[UUID(object_id)].type)

        if isinstance(annotation, Bbox):
            object_data[object_id].object_data.bbox.append(json_annotation)  # type: ignore

        elif isinstance(annotation, Cuboid):
            object_data[object_id].object_data.cuboid.append(json_annotation)  # type: ignore

        elif isinstance(annotation, Poly2d):
            object_data[object_id].object_data.poly2d.append(json_annotation)  # type: ignore

        elif isinstance(annotation, Poly3d):
            object_data[object_id].object_data.poly3d.append(json_annotation)  # type: ignore

        elif isinstance(annotation, Seg3d):
            object_data[object_id].object_data.vec.append(json_annotation)  # type: ignore

        else:
            raise TypeError

    for object_id in object_data:
        object_data[object_id].object_data.bbox = _empty_list_to_none(
            object_data[object_id].object_data.bbox
        )
        object_data[object_id].object_data.cuboid = _empty_list_to_none(
            object_data[object_id].object_data.cuboid
        )
        object_data[object_id].object_data.poly2d = _empty_list_to_none(
            object_data[object_id].object_data.poly2d
        )
        object_data[object_id].object_data.poly3d = _empty_list_to_none(
            object_data[object_id].object_data.poly3d
        )
        object_data[object_id].object_data.vec = _empty_list_to_none(
            object_data[object_id].object_data.vec
        )

    return object_data
