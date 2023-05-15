# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from .coordinate_system import CoordinateSystem
from .frame import Frame
from .metadata import Metadata


@dataclass
class Scene:
    """The root Understand.Ai class, which contains all data.

    Parameters
    ----------
    metadata: raillabel._understand_ai_t4_format.Metadata
        Container for metadata information about the scene itself.
    coordinate_systems: dict[str, raillabel._understand_ai_t4_format.CoordinateSystem]
        Global information for sensors regarding calibration.
    frames: dict[int, raillabel._understand_ai_t4_format.Frame]
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

    @classmethod
    def _coordinate_systems_fromdict(cls, data_dict: list[dict]) -> t.Dict[str, CoordinateSystem]:
        coordinate_systems = {}
        for cs in data_dict:
            coordinate_systems[cs["coordinate_system_id"]] = CoordinateSystem.fromdict(cs)

        return coordinate_systems

    @classmethod
    def _frames_fromdict(cls, data_dict: list[dict]) -> t.Dict[str, Frame]:
        frames = {}
        for frame in data_dict:
            frames[frame["frameId"]] = Frame.fromdict(frame)

        return frames
