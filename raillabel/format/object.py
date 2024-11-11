# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.json_format import JSONObject


@dataclass
class Object:
    """Physical, unique object in the data, that can be tracked via its UID."""

    name: str
    """Name of the object. It is a friendly name and not used for indexing. Commonly the class name
    is used followed by an underscore and an integer (i.e. person_0032)."""

    type: str
    "The type of an object defines the class the object corresponds to (like 'person')."

    @classmethod
    def from_json(cls, json: JSONObject) -> Object:
        """Construct an instant of this class from RailLabel JSON data."""
        return Object(
            name=json.name,
            type=json.type,
        )
