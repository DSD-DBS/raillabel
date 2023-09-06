# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from _collections_abc import dict_values

from .element_data_pointer import AttributeType, ElementDataPointer
from .frame_interval import FrameInterval

if t.TYPE_CHECKING:
    from .frame import Frame


@dataclass
class Object:
    """Physical, unique object in the data, that can be tracked via its UID.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier for the object.
    name: str
        Name of the object. It is a friendly name and not used for indexing. Commonly the class
        name is used followed by an underscore and an integer (i.e. person_0032).
    type: str
        The type of an object defines the class the object corresponds to.
    """

    uid: str
    name: str
    type: str

    # --- Public Methods --------------

    @classmethod
    def fromdict(cls, data_dict: dict, object_uid: str) -> "Object":
        """Generate a Object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        object_uid: str
            Unique identifier of the object.

        Returns
        -------
        object: raillabel.format.Object
            Converted object.
        """
        return Object(uid=object_uid, type=data_dict["type"], name=data_dict["name"])

    def asdict(self, frames: t.Optional[t.Dict[int, "Frame"]] = None) -> dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this class instance.
        frames: dict, optional
            The dictionary of frames stored under Scene.frames used for the frame intervals and
            object data pointers. If None, these are not provided. Default is None.

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.
        """

        if frames is None:
            return {"name": str(self.name), "type": str(self.type)}

        else:
            return {
                "name": str(self.name),
                "type": str(self.type),
                "frame_intervals": self._frame_intervals_asdict(self.frame_intervals(frames)),
                "object_data_pointers": self._object_data_pointers_asdict(
                    self.object_data_pointers(frames)
                ),
            }

    def frame_intervals(self, frames: t.Dict[int, "Frame"]) -> t.List[FrameInterval]:
        """Return frame intervals in which this object is present.

        Parameters
        ----------
        frames: dict[int, raillabel.format.Frame]
            The dictionary of frames stored under Scene.frames.

        Returns
        -------
        list[FrameInterval]
            List of the FrameIntervals, where this object is contained.
        """

        frame_uids_containing_object = [
            frame.uid for frame in frames.values() if self._is_object_in_frame(frame)
        ]

        return FrameInterval.from_frame_uids(frame_uids_containing_object)

    def object_data_pointers(self, frames: t.Dict[int, "Frame"]) -> t.Dict[str, ElementDataPointer]:
        """Create object data pointers used in WebLABEL visualization.

        Parameters
        ----------
        frames: dict[int, raillabel.format.Frame]
            The dictionary of frames stored under Scene.frames.

        Returns
        -------
        dict[str, ElementDataPointer]
            ObjectDataPointers dict as required by WebLABEL. Keys are the ObjectDataPointer uids.
        """

        pointer_ids_per_frame = self._collect_pointer_ids_per_frame(frames)
        frame_uids_per_pointer_id = self._reverse_frame_pointer_ids(pointer_ids_per_frame)
        frame_intervals_per_pointer_id = self._convert_to_intervals(frame_uids_per_pointer_id)

        attributes_per_pointer_id = self._collect_attributes_per_pointer_id(frames)
        attribute_pointers_per_pointer_id = self._convert_to_attribute_pointers(
            attributes_per_pointer_id
        )

        return self._create_object_data_pointers(
            frame_intervals_per_pointer_id, attribute_pointers_per_pointer_id
        )

    # --- Private Methods -------------

    def _frame_intervals_asdict(self, frame_intervals: t.List[FrameInterval]) -> dict:
        return [fi.asdict() for fi in frame_intervals]

    def _object_data_pointers_asdict(
        self, object_data_pointers: t.Dict[str, ElementDataPointer]
    ) -> dict:
        return {
            pointer_id: pointer.asdict() for pointer_id, pointer in object_data_pointers.items()
        }

    def _is_object_in_frame(self, frame: "Frame") -> bool:
        return self.uid in frame.object_data

    def _filtered_annotations(self, frame: "Frame") -> dict_values:
        return [ann for ann in frame.annotations.values() if ann.object.uid == self.uid]

    def _collect_pointer_ids_per_frame(
        self, frames: t.Dict[int, "Frame"]
    ) -> t.Dict[int, t.Set[str]]:

        pointer_ids_per_frame = {}
        for frame in frames.values():
            pointer_ids_per_frame[frame.uid] = set()

            for annotation in self._filtered_annotations(frame):
                pointer_ids_per_frame[frame.uid].add(annotation.name)

        return pointer_ids_per_frame

    def _reverse_frame_pointer_ids(
        self, pointer_ids_per_frame: t.Dict[int, t.Set[str]]
    ) -> t.Dict[str, t.Set[int]]:

        frame_uids_per_pointer_id = {}
        for frame_uid, pointer_ids in pointer_ids_per_frame.items():
            for pointer_id in pointer_ids:

                if pointer_id not in frame_uids_per_pointer_id:
                    frame_uids_per_pointer_id[pointer_id] = set()

                frame_uids_per_pointer_id[pointer_id].add(frame_uid)

        return frame_uids_per_pointer_id

    def _convert_to_intervals(
        self, frame_uids_per_pointer_id: t.Dict[str, t.Set[int]]
    ) -> t.Dict[str, t.List[FrameInterval]]:

        frame_intervals = {}
        for pointer_id, frame_uids in frame_uids_per_pointer_id.items():
            frame_intervals[pointer_id] = FrameInterval.from_frame_uids(list(frame_uids))

        return frame_intervals

    def _collect_attributes_per_pointer_id(
        self, frames: t.Dict[int, "Frame"]
    ) -> t.Dict[str, t.Dict[str, t.Any]]:

        attributes_per_pointer_id = {}
        for frame in frames.values():
            for annotation in self._filtered_annotations(frame):
                if annotation.name not in attributes_per_pointer_id:
                    attributes_per_pointer_id[annotation.name] = {}

                attributes_per_pointer_id[annotation.name].update(annotation.attributes)

        return attributes_per_pointer_id

    def _convert_to_attribute_pointers(
        self, attributes_per_pointer_id: t.Dict[str, t.Dict[str, t.Any]]
    ) -> t.Dict[str, t.Dict[str, AttributeType]]:
        for attributes in attributes_per_pointer_id.values():
            for attribute_name, attribute_value in attributes.items():
                attributes[attribute_name] = AttributeType.from_value(type(attribute_value))

        return attributes_per_pointer_id

    def _create_object_data_pointers(
        self,
        frame_intervals_per_pointer_id: t.Dict[str, t.List[FrameInterval]],
        attribute_pointers_per_pointer_id: t.Dict[str, t.Dict[str, AttributeType]],
    ) -> t.Dict[str, ElementDataPointer]:

        object_data_pointers = {}
        for pointer_id in frame_intervals_per_pointer_id:
            object_data_pointers[pointer_id] = ElementDataPointer(
                uid=pointer_id,
                frame_intervals=frame_intervals_per_pointer_id[pointer_id],
                attribute_pointers=attribute_pointers_per_pointer_id[pointer_id],
            )

        return object_data_pointers

    # --- Special Methods -------------

    def __hash__(self) -> int:
        """Return hash."""
        return self.uid.__hash__()
