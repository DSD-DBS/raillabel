# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.json_format import JSONTransformData

from .transform import Transform


@dataclass
class _SensorWithoutIntrinsics:
    """Parent class of all sensors, that do not have an intrinsic calibration."""

    extrinsics: Transform | None = None
    "External calibration of the sensor defined by the 3D transform to the coordinate system origin."

    uri: str | None = None
    "Name of the subdirectory containing the sensor files."

    description: str | None = None
    "Additional information about the sensor."


def _extrinsics_from_json(json_transform: JSONTransformData | None) -> Transform | None:
    if json_transform is None:
        return None
    return Transform.from_json(json_transform)
