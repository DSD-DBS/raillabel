# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from ..._util._warning import _warning
from .coordinate_system import CoordinateSystem
from .frame import Frame
from .metadata import Metadata


@dataclass
class Scene:
    """The root Understand.Ai class, which contains all data.

    Parameters
    ----------
    metadata: raillabel.format.understand_ai.Metadata
        Container for metadata information about the scene itself.
    coordinate_systems: dict[str, raillabel.format.understand_ai.CoordinateSystem]
        Global information for sensors regarding calibration.
    frames: dict[int, raillabel.format.understand_ai.Frame]
    """

    metadata: Metadata
    coordinate_systems: t.Dict[str, CoordinateSystem]
    frames: t.Dict[int, Frame]

    @classmethod
    def fromdict(cls, data_dict: dict) -> "Scene":
        """Generate a Scene from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        Scene
            Converted scene.
        """

        return Scene(
            metadata=Metadata.fromdict(data_dict["metadata"]),
            coordinate_systems=cls._coordinate_systems_fromdict(data_dict["coordinateSystems"]),
            frames=cls._frames_fromdict(data_dict["frames"]),
        )

    def to_raillabel(self) -> dict:
        """Convert to a raillabel compatible dict.

        Returns
        -------
        dict:
            Dictionary of the raillabel scene.
        """
        return {
            "openlabel": {
                "metadata": self.metadata.to_raillabel(),
                "streams": self._streams_to_raillabel(),
                "coordinate_systems": self._coordinate_systems_to_raillabel(),
                "objects": self._objects_to_raillabel(),
                "frames": {str(frame.id): frame.to_raillabel() for frame in self.frames.values()},
            }
        }

    @classmethod
    def _coordinate_systems_fromdict(cls, data_dict: t.List[dict]) -> t.Dict[str, CoordinateSystem]:
        coordinate_systems = {}
        for cs in data_dict:
            coordinate_systems[cs["coordinate_system_id"]] = CoordinateSystem.fromdict(cs)

        return coordinate_systems

    @classmethod
    def _frames_fromdict(cls, data_dict: t.List[dict]) -> t.Dict[int, Frame]:
        frames = {}
        for frame in data_dict:
            frame_id = int(frame["frameId"])

            if frame_id in frames:
                _warning(
                    f"Frame UID {frame_id} is contained more than once in the scene. "
                    + "The duplicate frame will be omitted."
                )
                continue

            frames[frame_id] = Frame.fromdict(frame)

        return frames

    def _streams_to_raillabel(self) -> dict:
        return {cs.translated_uid: cs.to_raillabel()[1] for cs in self.coordinate_systems.values()}

    def _coordinate_systems_to_raillabel(self) -> dict:
        coordinate_systems = {
            cs.translated_uid: cs.to_raillabel()[0] for cs in self.coordinate_systems.values()
        }

        coordinate_systems["base"] = {
            "type": "local",
            "parent": "",
            "children": list(coordinate_systems.keys()),
        }

        return coordinate_systems

    def _objects_to_raillabel(self) -> dict:

        object_dicts = self._collect_all_translated_objects()

        object_name_counter = {}
        objects = {}
        for object_id, object_class in object_dicts.items():

            if object_class not in object_name_counter:
                object_name_counter[object_class] = 0

            objects[object_id] = {
                "name": f"{object_class}_{str(object_name_counter[object_class]).rjust(4, '0')}",
                "type": object_class,
            }
            object_name_counter[object_class] += 1

        return objects

    def _collect_all_translated_objects(self) -> dict:
        object_dicts = {}
        for frame in self.frames.values():
            object_dicts.update(frame.translated_objects)

        return object_dicts
