# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass
from enum import Enum

from .intrinsics_pinhole import IntrinsicsPinhole
from .intrinsics_radar import IntrinsicsRadar
from .point3d import Point3d
from .quaternion import Quaternion
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
    intrinsics: raillabel.format.IntrinsicsPinhole or raillabel.format.IntrinsicsRadar, optional
        The intrinsic calibration of the sensor. Default is None.
    type: raillabel.format.SensorType, optional
        Information about the kind of sensor. Default is None.
    uri: str, optional
        Name of the subdirectory containing the sensor files. Default is None.
    description: str, optional
        Description of the sensor. Default is None.
    """

    uid: str
    extrinsics: t.Optional[Transform] = None
    intrinsics: t.Optional[t.Union[IntrinsicsPinhole, IntrinsicsRadar]] = None
    type: t.Optional["SensorType"] = None
    uri: t.Optional[str] = None
    description: t.Optional[str] = None

    @classmethod
    def fromdict(cls, uid: str, cs_data_dict: dict, stream_data_dict: dict) -> "Sensor":
        """Generate a Sensor object from a dict.

        Parameters
        ----------
        uid: str
            Unique identifier of the sensor.
        cs_data_dict: dict
            RailLabel format dict containing the data about the coordinate system.
        stream_data_dict: dict
            RailLabel format dict containing the data about the stream.

        Returns
        -------
        sensor: raillabel.format.Sensor
            Converted Sensor object.
        """

        return Sensor(
            uid=uid,
            extrinsics=cls._extrinsics_fromdict(cs_data_dict),
            intrinsics=cls._intrinsics_fromdict(
                stream_data_dict, cls._type_fromdict(stream_data_dict)
            ),
            type=cls._type_fromdict(stream_data_dict),
            uri=stream_data_dict.get("uri"),
            description=stream_data_dict.get("description"),
        )

    def asdict(self) -> dict:
        """Export self as a dict compatible with the RailLabel schema.

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
            stream_repr["type"] = str(self.type.value)

        if self.uri is not None:
            stream_repr["uri"] = str(self.uri)

        if self.description is not None:
            stream_repr["description"] = str(self.description)

        if isinstance(self.intrinsics, IntrinsicsPinhole):
            stream_repr["stream_properties"] = {"intrinsics_pinhole": self.intrinsics.asdict()}

        elif isinstance(self.intrinsics, IntrinsicsRadar):
            stream_repr["stream_properties"] = {"intrinsics_radar": self.intrinsics.asdict()}

        return stream_repr

    @classmethod
    def _extrinsics_fromdict(cls, data_dict) -> t.Optional[Transform]:

        if "pose_wrt_parent" not in data_dict:
            return None

        return Transform(
            pos=Point3d(
                x=data_dict["pose_wrt_parent"]["translation"][0],
                y=data_dict["pose_wrt_parent"]["translation"][1],
                z=data_dict["pose_wrt_parent"]["translation"][2],
            ),
            quat=Quaternion(
                x=data_dict["pose_wrt_parent"]["quaternion"][0],
                y=data_dict["pose_wrt_parent"]["quaternion"][1],
                z=data_dict["pose_wrt_parent"]["quaternion"][2],
                w=data_dict["pose_wrt_parent"]["quaternion"][3],
            ),
        )

    @classmethod
    def _intrinsics_fromdict(
        cls, data_dict, sensor_type: t.Optional["SensorType"]
    ) -> t.Optional[IntrinsicsPinhole]:

        if "stream_properties" not in data_dict:
            return None

        if sensor_type == SensorType.CAMERA:

            if "intrinsics_pinhole" in data_dict["stream_properties"]:
                return IntrinsicsPinhole.fromdict(
                    data_dict["stream_properties"]["intrinsics_pinhole"]
                )

        elif sensor_type == SensorType.RADAR:

            if "intrinsics_radar" in data_dict["stream_properties"]:
                return IntrinsicsRadar.fromdict(data_dict["stream_properties"]["intrinsics_radar"])

        return None

    @classmethod
    def _type_fromdict(cls, data_dict) -> t.Optional["SensorType"]:

        if "type" not in data_dict:
            return None

        return SensorType(data_dict["type"])


class SensorType(Enum):
    """Enumeration representing all possible sensor types."""

    CAMERA = "camera"
    LIDAR = "lidar"
    RADAR = "radar"
    GPS_IMU = "gps_imu"
    OTHER = "other"
