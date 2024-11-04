# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.json_format import JSONIntrinsicsPinhole


@dataclass
class IntrinsicsPinhole:
    """Intrinsic calibration for a camera sensor."""

    camera_matrix: tuple[
        float, float, float, float, float, float, float, float, float, float, float, float
    ]
    """This is a 3x4 camera matrix which projects 3D homogeneous points (4x1) from a camera
    coordinate system into the image plane (3x1). This is the usual K matrix for camera projection as
    in OpenCV. It is extended from 3x3 to 3x4 to enable its direct utilisation to project 4x1
    homogeneous 3D points. The matrix is defined to follow the camera model: x-to-right, y-down,
    z-forward. The following equation applies: x_img = camera_matrix * X_ccs."""

    distortion: tuple[float, float, float, float, float]
    "This is the array 1x5 radial and tangential distortion coefficients."

    width_px: int
    "Width of the image frame in pixel."

    height_px: int
    "Height of the image frame in pixel."

    @classmethod
    def from_json(cls, json: JSONIntrinsicsPinhole) -> IntrinsicsPinhole:
        """Construct an instant of this class from RailLabel JSON data."""
        return IntrinsicsPinhole(
            camera_matrix=json.camera_matrix,
            distortion=json.distortion_coeffs,
            width_px=json.width_px,
            height_px=json.height_px,
        )

    @classmethod
    def fromdict(cls, data_dict: dict) -> IntrinsicsPinhole:
        """Generate a IntrinsicsPinhole object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.

        Returns
        -------
        raillabel.format.IntrinsicsPinhole
            Converted IntrinsicsPinhole object.

        """
        return IntrinsicsPinhole(
            camera_matrix=tuple(data_dict["camera_matrix"]),
            distortion=tuple(data_dict["distortion_coeffs"]),
            width_px=data_dict["width_px"],
            height_px=data_dict["height_px"],
        )

    def asdict(self) -> dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this class instance.

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.

        """
        return {
            "camera_matrix": list(self.camera_matrix),
            "distortion_coeffs": list(self.distortion),
            "width_px": int(self.width_px),
            "height_px": int(self.height_px),
        }
