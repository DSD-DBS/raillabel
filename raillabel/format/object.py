# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from raillabel.json_format import JSONElementDataPointer, JSONFrameInterval, JSONObject

from ._attributes import _attributes_to_json
from .frame_interval import FrameInterval

if TYPE_CHECKING:
    from .frame import Frame


@dataclass
class Object:
    """Physical, unique object in the data, that can be tracked via its UID."""

    name: str
    """Name of the object. It is a friendly name and not used for indexing. Commonly the class name
    is used followed by an underscore and an integer (i.e. person_0032)."""

    type: str
    "The type of an object defines the class the object corresponds to (like 'person')."

    @classmethod
    def from_json(cls, json: JSONObject) -> Object:
        """Construct an instant of this class from RailLabel JSON data."""
        return Object(
            name=json.name,
            type=json.type,
        )

    def to_json(self, object_id: UUID, frames: dict[int, Frame]) -> JSONObject:
        """Export this object into the RailLabel JSON format."""
        return JSONObject(
            name=self.name,
            type=self.type,
            frame_intervals=_frame_intervals_to_json(object_id, frames),
            object_data_pointers=_object_data_pointers_to_json(object_id, self.type, frames),
        )


def _frame_intervals_to_json(object_id: UUID, frames: dict[int, Frame]) -> list[JSONFrameInterval]:
    frames_with_this_object = set()

    for frame_id, frame in frames.items():
        for annotation in frame.annotations.values():
            if annotation.object_id == object_id:
                frames_with_this_object.add(frame_id)
                continue

    return [fi.to_json() for fi in FrameInterval.from_frame_ids(list(frames_with_this_object))]


def _object_data_pointers_to_json(
    object_id: UUID, object_type: str, frames: dict[int, Frame]
) -> dict[str, JSONElementDataPointer]:
    pointers_raw = {}

    for frame_id, frame in frames.items():
        for annotation in [ann for ann in frame.annotations.values() if ann.object_id == object_id]:
            annotation_name = annotation.name(object_type)
            if annotation_name not in pointers_raw:
                pointers_raw[annotation_name] = {
                    "frame_intervals": set(),
                    "type": annotation_name.split("__")[1],
                    "attribute_pointers": {},
                }

            pointers_raw[annotation_name]["frame_intervals"].add(frame_id)  # type: ignore
            json_attributes = _attributes_to_json(annotation.attributes)

            if json_attributes is None:
                continue

            for attribute in json_attributes.boolean:  # type: ignore
                pointers_raw[annotation_name]["attribute_pointers"][attribute.name] = "boolean"  # type: ignore

            for attribute in json_attributes.num:  # type: ignore
                pointers_raw[annotation_name]["attribute_pointers"][attribute.name] = "num"  # type: ignore

            for attribute in json_attributes.text:  # type: ignore
                pointers_raw[annotation_name]["attribute_pointers"][attribute.name] = "text"  # type: ignore

            for attribute in json_attributes.vec:  # type: ignore
                pointers_raw[annotation_name]["attribute_pointers"][attribute.name] = "vec"  # type: ignore

    object_data_pointers = {}
    for annotation_name, object_data_pointer in pointers_raw.items():
        object_data_pointers[annotation_name] = JSONElementDataPointer(
            type=object_data_pointer["type"],
            frame_intervals=[
                fi.to_json()
                for fi in FrameInterval.from_frame_ids(list(object_data_pointer["frame_intervals"]))  # type: ignore
            ],
            attribute_pointers=object_data_pointer["attribute_pointers"],
        )

    return object_data_pointers
