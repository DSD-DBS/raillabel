# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

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