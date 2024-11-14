# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from raillabel.json_format import JSONStreamSync, JSONStreamSyncProperties, JSONStreamSyncTimestamp


@dataclass
class SensorReference:
    """A reference to a sensor in a specific frame."""

    timestamp: Decimal
    """Timestamp containing the Unix epoch time of the sensor in a specific frame with up to
    nanosecond precision."""

    uri: str | None = None
    "URI to the file corresponding to the frame recording in the particular frame."

    @classmethod
    def from_json(cls, json: JSONStreamSync) -> SensorReference:
        """Construct an instant of this class from RailLabel JSON data."""
        return SensorReference(
            timestamp=Decimal(json.stream_properties.sync.timestamp),
            uri=json.uri,
        )

    def to_json(self) -> JSONStreamSync:
        """Export this object into the RailLabel JSON format."""
        return JSONStreamSync(
            stream_properties=JSONStreamSyncProperties(
                sync=JSONStreamSyncTimestamp(timestamp=str(self.timestamp)),
            ),
            uri=self.uri,
        )
