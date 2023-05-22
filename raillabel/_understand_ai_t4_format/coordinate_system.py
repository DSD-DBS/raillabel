# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass


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
        Distortion coefficients of the sensor. Only applies to sensors of type camera. Default is None.
    """

    uid: str
    topic: str
    frame_id: str
    position: t.List[float]
    rotation_quaternion: t.List[float]
    rotation_matrix: t.List[float]
    angle_axis_rotation: t.List[float]
    homogeneous_transform: t.Optional[t.List[float]]
    measured_position: t.Optional[t.List[float]]
    camera_matrix: t.Optional[t.List[float]]
    dist_coeffs: t.Optional[t.List[float]]

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
