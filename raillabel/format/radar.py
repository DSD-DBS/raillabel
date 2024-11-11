# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.json_format import JSONCoordinateSystem, JSONStreamRadar, JSONTransformData

from .intrinsics_radar import IntrinsicsRadar
from .transform import Transform


@dataclass
class Radar:
    """A radar sensor."""

    intrinsics: IntrinsicsRadar
    "The intrinsic calibration of the sensor."

    extrinsics: Transform | None = None
    "External calibration of the sensor defined by the 3D transform to the coordinate system origin."

    uri: str | None = None
    "Name of the subdirectory containing the sensor files."

    description: str | None = None
    "Additional information about the sensor."

    @classmethod
    def from_json(
        cls, json_stream: JSONStreamRadar, json_coordinate_system: JSONCoordinateSystem
    ) -> Radar:
        """Construct an instant of this class from RailLabel JSON data."""
        return Radar(
            intrinsics=IntrinsicsRadar.from_json(json_stream.stream_properties.intrinsics_radar),
            extrinsics=_extrinsics_from_json(json_coordinate_system.pose_wrt_parent),
            uri=json_stream.uri,
            description=json_stream.description,
        )


def _extrinsics_from_json(json_transform: JSONTransformData | None) -> Transform | None:
    if json_transform is None:
        return None
    return Transform.from_json(json_transform)
