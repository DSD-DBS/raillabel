# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from raillabel.json_format import JSONCoordinateSystem, JSONStreamOther

from ._sensor_without_intrinsics import _extrinsics_from_json, _SensorWithoutIntrinsics


class OtherSensor(_SensorWithoutIntrinsics):
    """A sensor that is not represented by the available options."""

    TYPE: str = "other"

    @classmethod
    def from_json(
        cls, json_stream: JSONStreamOther, json_coordinate_system: JSONCoordinateSystem
    ) -> OtherSensor:
        """Construct an instant of this class from RailLabel JSON data."""
        return OtherSensor(
            extrinsics=_extrinsics_from_json(json_coordinate_system.pose_wrt_parent),
            uri=json_stream.uri,
            description=json_stream.description,
        )

    def to_json(self) -> tuple[JSONStreamOther, JSONCoordinateSystem]:
        """Export this object into the RailLabel JSON format."""
        return (
            JSONStreamOther(
                type="other",
                uri=self.uri,
                description=self.description,
            ),
            JSONCoordinateSystem(
                parent="base",
                type="sensor",
                pose_wrt_parent=self.extrinsics.to_json() if self.extrinsics is not None else None,
            ),
        )
