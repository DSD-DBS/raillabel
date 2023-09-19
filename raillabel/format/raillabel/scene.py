# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass, field

from ... import exceptions
from ..._util._clean_dict import _clean_dict
from ..._util._warning import _warning
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
    objects: t.Dict[str, Object] = field(default_factory=dict)
    frames: t.Dict[int, Frame] = field(default_factory=dict)

    @property
    def frame_intervals(self) -> t.List[FrameInterval]:
        """Return frame intervals of the present frames."""
        return FrameInterval.from_frame_uids(list(self.frames.keys()))

    # === Public Methods ==========================================================================

    @classmethod
    def fromdict(cls, data_dict: dict, subschema_version: t.Optional[str] = None) -> "Scene":
        """Generate a Scene object from a RailLABEL-dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        subschema_version: str, optional
            Version of the RailLabel subschema.

        Returns
        -------
        raillabel.format.Scene
            Converted Scene object.

        Raises
        ------
        raillabel.exceptions.MissingCoordinateSystemError
            if a stream has no corresponding coordinate system.
        raillabel.exceptions.MissingStreamError
            if a coordinate system has no corresponding stream.
        raillabel.exceptions.UnsupportedParentError
            if a coordinate system has no corresponding stream.
        """

        data_dict = cls._prepare_data(data_dict)

        sensors = cls._sensors_fromdict(data_dict["streams"], data_dict["coordinate_systems"])
        objects = cls._objects_fromdict(data_dict["objects"])

        return Scene(
            metadata=Metadata.fromdict(data_dict["metadata"], subschema_version),
            sensors=sensors,
            objects=objects,
            frames=cls._frames_fromdict(data_dict["frames"], sensors, objects),
        )

    def asdict(self, calculate_pointers: bool = True) -> dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this Scene.
        calculate_pointers: bool, optional
            If True, object_data_pointers and Object frame_intervals will be calculated. Default
            is True.

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.
        """

        return {
            "openlabel": _clean_dict(
                {
                    "metadata": self.metadata.asdict(),
                    "streams": self._streams_asdict(self.sensors),
                    "coordinate_systems": self._coordinate_systems_asdict(self.sensors),
                    "objects": self._objects_asdict(self.objects, calculate_pointers),
                    "frames": self._frames_asdict(self.frames),
                    "frame_intervals": self._frame_intervals_asdict(self.frame_intervals),
                }
            )
        }

    # === Private Methods =========================================================================

    # --- fromdict() ----------------------------

    @classmethod
    def _prepare_data(cls, data: dict) -> dict:
        """Add optional fields to dict to simplify interaction.

        Parameters
        ----------
        data : dict
            JSON data.

        Returns
        -------
        dict
            Enhanced JSON data.
        """

        if "coordinate_systems" not in data["openlabel"]:
            data["openlabel"]["coordinate_systems"] = {}

        if "streams" not in data["openlabel"]:
            data["openlabel"]["streams"] = {}

        if "objects" not in data["openlabel"]:
            data["openlabel"]["objects"] = {}

        if "frames" not in data["openlabel"]:
            data["openlabel"]["frames"] = {}

        return data["openlabel"]

    @classmethod
    def _sensors_fromdict(
        cls, streams_dict: dict, coordinate_systems_dict: dict
    ) -> t.Dict[str, Sensor]:

        cls._check_sensor_completeness(streams_dict, coordinate_systems_dict)

        sensors = {}

        for stream_id in streams_dict:
            sensors[stream_id] = Sensor.fromdict(
                uid=stream_id,
                cs_data_dict=coordinate_systems_dict[stream_id],
                stream_data_dict=streams_dict[stream_id],
            )

        return sensors

    @classmethod
    def _check_sensor_completeness(cls, streams_dict: dict, coordinate_systems_dict: dict):

        for stream_uid in streams_dict:
            if stream_uid not in coordinate_systems_dict:
                raise exceptions.MissingCoordinateSystemError(
                    f"Stream {stream_uid} has no corresponding coordinate system."
                )

        for cs_uid in coordinate_systems_dict:
            if cs_uid == "base":
                continue

            if coordinate_systems_dict[cs_uid]["parent"] != "base":
                raise exceptions.UnsupportedParentError(
                    f"Only 'base' is permitted as a parent for coordinate system {cs_uid}, "
                    + f"not {coordinate_systems_dict[cs_uid]['parent']}."
                )

            if cs_uid not in streams_dict:
                raise exceptions.MissingStreamError(
                    f"Coordinate sytem {cs_uid} has no corresponding stream."
                )

    @classmethod
    def _objects_fromdict(cls, object_dict: dict) -> t.Dict[str, Object]:
        return {uid: Object.fromdict(object, uid) for uid, object in object_dict.items()}

    @classmethod
    def _frames_fromdict(
        cls, frames_dict: dict, sensors: t.Dict[str, Sensor], objects: t.Dict[str, Object]
    ) -> t.Dict[int, Frame]:

        frames = {}
        for frame_uid, frame_dict in frames_dict.items():
            frame_uid = int(frame_uid)

            if frame_uid in frames:
                _warning(
                    f"Frame UID {frame_uid} is contained more than once in the scene. "
                    + "The duplicate frame will be omitted."
                )
                continue

            frames[frame_uid] = Frame.fromdict(frame_uid, frame_dict, objects, sensors)

        return frames

    # --- asdict() ------------------------------

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

    def _objects_asdict(self, objects: t.Dict[str, Object], calculate_pointers: bool) -> dict:

        if calculate_pointers:
            return {str(uid): object.asdict(self.frames) for uid, object in objects.items()}
        else:
            return {str(uid): object.asdict() for uid, object in objects.items()}

    def _frames_asdict(self, frames: t.Dict[int, Frame]) -> dict:
        return {str(uid): frame.asdict() for uid, frame in frames.items()}

    def _frame_intervals_asdict(self, frame_intervals: t.List[FrameInterval]) -> t.List[dict]:
        return [fi.asdict() for fi in frame_intervals]
