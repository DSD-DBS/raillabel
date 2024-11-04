# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .intrinsics_pinhole import IntrinsicsPinhole
from .intrinsics_radar import IntrinsicsRadar
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
    extrinsics: Transform | None = None
    intrinsics: IntrinsicsPinhole | IntrinsicsRadar | None = None
    type: SensorType | None = None
    uri: str | None = None
    description: str | None = None


class SensorType(Enum):
    """Enumeration representing all possible sensor types."""

    CAMERA = "camera"
    LIDAR = "lidar"
    RADAR = "radar"
    GPS_IMU = "gps_imu"
    OTHER = "other"
