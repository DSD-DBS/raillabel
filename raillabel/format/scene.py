# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
import uuid
from dataclasses import dataclass, field

from .frame import Frame
from .frame_interval import FrameInterval
from .metadata import Metadata
from .object import Object
from .sensor import Sensor


@dataclass
class Scene:
    """The root RailLabel class, which contains all data.

    Parameters
    ----------
    metadata: raillabel.format.Metadata
        This object contains information, that is, metadata, about the annotation file itself.
    sensors: dict of raillabel.format.Sensor, optional
        Dictionary of raillabel.format.Sensors. Dictionary keys are the sensor uids. Default is {}.
    objects: dict of raillabel.format.Object, optional
        Dictionary of raillabel.format.Objects. Dictionary keys are the object uids. Default is {}.
    frames: dict of raillabel.format.Frame, optional
        Dict of frames in the scene. Dictionary keys are the frame uids. Default is {}.

    Properties (read-only)
    ----------------------
    frame_intervals: list[FrameIntervals]
        List of frame intervals describing the frames present in this scene.
    """

    metadata: Metadata
    sensors: t.Dict[str, Sensor] = field(default_factory=dict)
    objects: t.Dict[uuid.UUID, Object] = field(default_factory=dict)
    frames: t.Dict[int, Frame] = field(default_factory=dict)

    @property
    def frame_intervals(self) -> t.List[FrameInterval]:
        """Return frame intervals of the present frames."""
        return FrameInterval.from_frame_uids(list(self.frames.keys()))

    def asdict(self) -> dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this Scene.

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.
        """

        return {
            "openlabel": self._clean_empty_fields(
                {
                    "metadata": self.metadata.asdict(),
                    "streams": self._streams_asdict(self.sensors),
                    "coordinate_systems": self._coordinate_systems_asdict(self.sensors),
                    "objects": self._objects_asdict(self.objects),
                    "frames": self._frames_asdict(self.frames),
                    "frame_intervals": self._frame_intervals_asdict(self.frame_intervals),
                }
            )
        }

    def _clean_empty_fields(self, dictionary: dict) -> dict:

        empty_keys = []
        for key, value in dictionary.items():
            if value is None or len(value) == 0:
                empty_keys.append(key)

        for key in empty_keys:
            del dictionary[key]

        return dictionary

    def _streams_asdict(self, sensors: t.Dict[str, Sensor]) -> dict:
        return {uid: sensor.asdict()["stream"] for uid, sensor in sensors.items()}

    def _coordinate_systems_asdict(self, sensors: t.Dict[str, Sensor]) -> dict:

        if len(sensors) == 0:
            return None

        coordinate_systems = {"base": {"type": "local", "parent": "", "children": []}}

        for uid, sensor in sensors.items():
            coordinate_systems[uid] = sensor.asdict()["coordinate_system"]
            coordinate_systems["base"]["children"].append(uid)

        return coordinate_systems

    def _objects_asdict(self, objects: t.Dict[uuid.UUID, Object]) -> dict:
        return {str(uid): object.asdict(self.frames) for uid, object in objects.items()}

    def _frames_asdict(self, frames: t.Dict[int, Frame]) -> dict:
        return {uid: frame.asdict() for uid, frame in frames.items()}

    def _frame_intervals_asdict(self, frame_intervals: t.List[FrameInterval]) -> t.List[dict]:
        return [fi.asdict() for fi in frame_intervals]
