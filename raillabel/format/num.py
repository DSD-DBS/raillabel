# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.json_format import JSONNum


@dataclass
class Num:
    """A number."""

    name: str
    "Human readable name describing the annotation."

    val: float
    "This is the value of the number object."

    sensor_id: str | None
    "A reference to the sensor, this value is represented in."

    @classmethod
    def from_json(cls, json: JSONNum) -> Num:
        """Construct an instant of this class from RailLabel JSON data."""
        return Num(
            name=json.name,
            val=json.val,
            sensor_id=json.coordinate_system,
        )
