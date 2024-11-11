# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from ._sensor_without_intrinsics import _SensorWithoutIntrinsics


class GpsImu(_SensorWithoutIntrinsics):
    """A gps sensor with inertial measurement unit."""
