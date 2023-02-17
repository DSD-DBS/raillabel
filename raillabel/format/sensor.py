# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from .point3d import Point3d
from .quaternion import Quaternion
from .stream_calibration import StreamCalibration
from .transform import Transform


@dataclass
class Sensor:
    """A reference to a physical sensor on the train.

    A sensor in the devkit corresponds to one coordinate_system and one stream in the data format.
    This distinction is set by the OpenLABEL standard, but is not relevant for our data.
    Therefore, we decided to combine these fields.

    Parameters
    ----------
    uid: str
        This is the friendly name of the sensor as well as its identifier. Must be
        unique.
    extrinsics: raillabel.format.Transform, optional
        The external calibration of the sensor defined by the 3D transform to the coordinate
        system origin. Default is None.
    intrinsics: raillabel.format.StreamCalibration, optional
        The intrinsic calibration of the sensor. Default is None.
    type: str-enum
        A string encoding the type of the sensor. The only valid values are 'camera', 'lidar',
        'radar', 'gps_imu' or 'other'.
    rostopic: str, optional
        Name of the topic of the stream in ROS. Default is None.
    description: str, optional
        Description of the sensor. Default is None.
    """

    uid: str
    extrinsics: t.Optional[Transform] = None
    intrinsics: t.Optional[StreamCalibration] = None
    type: str = None
    rostopic: t.Optional[str] = None
    description: t.Optional[str] = None

    _VALID_SENSOR_TYPES = ["camera", "lidar", "radar", "gps_imu", "other"]

    @classmethod
    def fromdict(self, uid: str, cs_raw: dict, stream_raw: dict) -> t.Tuple["Sensor", list]:
        """Generate a Sensor object from a dictionary in the OpenLABEL format.

        Parameters
        ----------
        uid: str
            Unique identifier of the sensor.
        cs_raw: dict
            OpenLABEL format dict containing the data about the coordinate system.
        stream_raw: dict
            OpenLABEL format dict containing the data about the stream.

        Returns
        -------
        sensor: raillabel.format.Sensor
            Converted Sensor object.
        warnings: list of str
            List of non-critical errors, that have occurred during the conversion.
        """

        warnings = []
        sensor = Sensor(uid)

        if "pose_wrt_parent" in cs_raw:
            sensor.extrinsics = Transform(
                pos=Point3d(
                    x=cs_raw["pose_wrt_parent"]["translation"][0],
                    y=cs_raw["pose_wrt_parent"]["translation"][1],
                    z=cs_raw["pose_wrt_parent"]["translation"][2],
                ),
                quat=Quaternion(
                    x=cs_raw["pose_wrt_parent"]["quaternion"][0],
                    y=cs_raw["pose_wrt_parent"]["quaternion"][1],
                    z=cs_raw["pose_wrt_parent"]["quaternion"][2],
                    w=cs_raw["pose_wrt_parent"]["quaternion"][3],
                ),
            )

        if (
            "stream_properties" in stream_raw
            and "intrinsics_pinhole" in stream_raw["stream_properties"]
        ):
            sensor.intrinsics = StreamCalibration(
                camera_matrix=tuple(
                    stream_raw["stream_properties"]["intrinsics_pinhole"]["camera_matrix"]
                ),
                distortion=tuple(
                    stream_raw["stream_properties"]["intrinsics_pinhole"]["distortion_coeffs"]
                ),
                width_px=stream_raw["stream_properties"]["intrinsics_pinhole"]["width_px"],
                height_px=stream_raw["stream_properties"]["intrinsics_pinhole"]["height_px"],
            )

        if "type" in stream_raw:
            sensor.type = stream_raw["type"]

        if "uri" in stream_raw:
            sensor.rostopic = stream_raw["uri"]

        if "description" in stream_raw:
            sensor.type = stream_raw["description"]

        return sensor, warnings

    def asdict(self) -> dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this class instance.
        """

        return {
            "coordinate_system": self._as_coordinate_system_dict(),
            "stream": self._as_stream_dict(),
        }

    def _as_coordinate_system_dict(self) -> dict:

        coordinate_system_repr = {"type": "sensor", "parent": "base"}

        if self.extrinsics is not None:
            coordinate_system_repr["pose_wrt_parent"] = self.extrinsics.asdict()

        return coordinate_system_repr

    def _as_stream_dict(self) -> dict:

        stream_repr = {}

        if self.type is not None:
            if self.type not in self._VALID_SENSOR_TYPES:
                raise ValueError(
                    f"Sensor.type must be one of {self._VALID_SENSOR_TYPES}, not {self.type}."
                )

            stream_repr["type"] = str(self.type)

        if self.rostopic is not None:
            stream_repr["uri"] = str(self.rostopic)

        if self.description is not None:
            stream_repr["description"] = str(self.description)

        if self.intrinsics is not None:
            stream_repr["stream_properties"] = {"intrinsics_pinhole": self.intrinsics.asdict()}

        return stream_repr
