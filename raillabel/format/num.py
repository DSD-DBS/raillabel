# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from raillabel.json_format import JSONNum


@dataclass
class Num:
    """A number."""

    name: str
    "Human readable name describing the annotation."

    val: float
    "This is the value of the number object."

    id: UUID | None = None
    "The unique identifyer of the Num."

    sensor_id: str | None = None
    "A reference to the sensor, this value is represented in."

    @classmethod
    def from_json(cls, json: JSONNum) -> Num:
        """Construct an instant of this class from RailLabel JSON data."""
        return Num(
            name=json.name,
            val=json.val,
            id=json.uid,
            sensor_id=json.coordinate_system,
        )

    def to_json(self) -> JSONNum:
        """Export this object into the RailLabel JSON format."""
        return JSONNum(
            name=self.name,
            val=self.val,
            coordinate_system=self.sensor_id,
            uid=self.id,
        )
