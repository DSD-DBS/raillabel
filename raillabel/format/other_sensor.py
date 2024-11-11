# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from ._sensor_without_intrinsics import _SensorWithoutIntrinsics


class OtherSensor(_SensorWithoutIntrinsics):
    """A sensor that is not represented by the available options."""
