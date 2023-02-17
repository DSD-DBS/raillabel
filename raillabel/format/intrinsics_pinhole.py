# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass


@dataclass
class IntrinsicsPinhole:
    """Intrinsic calibration for a camera sensor.

    Parameters
    ----------
    camera_matrix: tuple of float of length 12
        This is a 3x4 camera matrix which projects 3D homogeneous points (4x1) from a camera
        coordinate system into the image plane (3x1). This is the usual K matrix for camera
        projection as in OpenCV. It is extended from 3x3 to 3x4 to enable its direct utilisation to
        project 4x1 homogeneous 3D points. The matrix is defined to follow the camera model:
        x-to-right, y-down, z-forward. The following equation applies: x_img = camera_matrix * X_ccs.
    distortion: tuple of float of length 5 to 14
        This is the array 1xN radial and tangential distortion coefficients.
    width_px: int
        Width of the image frame in pixels.
    height_px: int
        Height of the image frame in pixels.
    """

    camera_matrix: t.Tuple[float, ...]
    distortion: t.Tuple[float, ...]
    width_px: int
    height_px: int

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

        dict_repr = {
            "camera_matrix": list(self.camera_matrix),
            "distortion_coeffs": list(self.distortion),
            "width_px": int(self.width_px),
            "height_px": int(self.height_px),
        }

        return dict_repr
