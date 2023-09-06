# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SensorReference:
    """Information for a sensor in a frame.

    Parameters
    ----------
    type: str
        Friendly name of the sensor and its unique identifier.
    uri: str
        URI to the file containing the frame specific sensor output from the project directory.
    timestamp: decimal.Decimal
        Unix timestamp of the sensor recording.
    """

    type: str
    uri: str
    timestamp: Decimal

    @classmethod
    def fromdict(cls, data_dict: dict) -> "SensorReference":
        """Generate a SensorReference from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        SensorReference
            Converted sensor reference.
        """

        return SensorReference(
            type=data_dict["type"], uri=data_dict["uri"], timestamp=Decimal(data_dict["timestamp"])
        )

    def to_raillabel(self) -> t.Tuple[str, dict]:
        """Convert to a raillabel compatible dict.

        Returns
        -------
        sensor_id: str
            Friendly identifier of the sensor.
        sensor_reference: dict
            Dictionary valid for the raillabel schema.
        """

        return (
            self.type,
            {
                "stream_properties": {"sync": {"timestamp": str(self.timestamp)}},
                "uri": self.uri.split("/")[-1],
            },
        )
