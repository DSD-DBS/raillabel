# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from ._translation import fetch_sensor_resolutions, fetch_sensor_type, translate_sensor_id


@dataclass
class CoordinateSystem:
    """Global information for a sensor regarding calibration.

    Parameters
    ----------
    uid: str
        Friendly name of the sensor as well as its identifier. Must be unique
    topic: str
        Rostopic of the sensor.
    frame_id: str
        Name of the directory containing the files from this sensor.
    position: list of float
        3D translation with regards to the origin.
    rotation_quaternion: list of float
        Rotation quaternion with regards to the origin.
    rotation_matrix: list of float
        Rotation matrix with regards to the origin.
    angle_axis_rotation: list of float
        Angle axis rotation with regards to the origin.
    homogeneous_transform: list of float, optional
        Homogeneous transformation matrix with regards to the origin. Default is None.
    measured_position: list of float, optional
    camera_matrix: list of float, optional
        Camera matrix of the sensor. Only applies to sensors of type camera. Default is None.
    dist_coeffs: list of float, optional
        Distortion coefficients of the sensor. Only applies to sensors of type camera. Default is
        None.
    """

    uid: str
    topic: str
    frame_id: str
    position: t.List[float]
    rotation_quaternion: t.List[float]
    rotation_matrix: t.List[float]
    angle_axis_rotation: t.List[float]
    homogeneous_transform: t.Optional[t.List[float]] = None
    measured_position: t.Optional[t.List[float]] = None
    camera_matrix: t.Optional[t.List[float]] = None
    dist_coeffs: t.Optional[t.List[float]] = None

    @property
    def translated_uid(self) -> str:
        """Return uid translated to raillabel."""
        return translate_sensor_id(self.uid)

    @classmethod
    def fromdict(cls, data_dict: dict) -> "CoordinateSystem":
        """Generate a CoordinateSystem from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data.

        Returns
        -------
        coordinate_system: CoordinateSystem
            Converted coordinate_system.
        """

        return CoordinateSystem(
            uid=data_dict["coordinate_system_id"],
            topic=data_dict["topic"],
            frame_id=data_dict["frame_id"],
            position=data_dict["position"],
            rotation_quaternion=data_dict["rotation_quaternion"],
            rotation_matrix=data_dict["rotation_matrix"],
            angle_axis_rotation=data_dict["angle_axis_rotation"],
            homogeneous_transform=data_dict.get("homogeneous_transform"),
            measured_position=data_dict.get("measured_position"),
            camera_matrix=data_dict.get("camera_matrix"),
            dist_coeffs=data_dict.get("dist_coeffs"),
        )

    def to_raillabel(self) -> t.Tuple[dict, dict]:
        """Convert to a raillabel compatible dict.

        Returns
        -------
        coordinate_system_dict: dict
            Dictionary of the raillabel coordinate system.
        stream_dict: dict
            Dictionary of the raillabel stream.
        """

        stream_dict = {
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": {
                "translation": self.position,
                "quaternion": self.rotation_quaternion,
            },
        }

        coordinate_system_dict = {
            "type": fetch_sensor_type(self.translated_uid),
            "uri": self.topic,
            "stream_properties": self._stream_properties_to_raillabel(
                fetch_sensor_type(self.translated_uid)
            ),
        }

        if coordinate_system_dict["stream_properties"] is None:
            del coordinate_system_dict["stream_properties"]

        return stream_dict, coordinate_system_dict

    def _stream_properties_to_raillabel(self, type: str) -> t.Optional[dict]:

        if type == "camera":
            return {
                "intrinsics_pinhole": {
                    "camera_matrix": self._convert_camera_matrix(self.camera_matrix[:]),
                    "distortion_coeffs": self.dist_coeffs,
                    "width_px": fetch_sensor_resolutions(self.translated_uid)["x"],
                    "height_px": fetch_sensor_resolutions(self.translated_uid)["y"],
                }
            }

        elif type == "radar":
            return {
                "intrinsics_radar": {
                    "resolution_px_per_m": fetch_sensor_resolutions(self.translated_uid)[
                        "resolution_px_per_m"
                    ],
                    "width_px": fetch_sensor_resolutions(self.translated_uid)["x"],
                    "height_px": fetch_sensor_resolutions(self.translated_uid)["y"],
                }
            }

        else:
            return None

    def _convert_camera_matrix(self, camera_matrix: list) -> list:

        camera_matrix.insert(9, 0)
        camera_matrix.insert(6, 0)
        camera_matrix.insert(3, 0)

        return camera_matrix
