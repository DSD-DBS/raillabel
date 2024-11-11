# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from ._sensor_without_intrinsics import _SensorWithoutIntrinsics


class Lidar(_SensorWithoutIntrinsics):
    """A lidar sensor."""
