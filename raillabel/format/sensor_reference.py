# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import decimal
from dataclasses import dataclass
from typing import Any

from .sensor import Sensor


@dataclass
class SensorReference:
    """A reference to a sensor in a specific frame.

    Parameters
    ----------
    sensor: raillabel.format.Sensor
        The sensor this SensorReference corresponds to.
    timestamp: decimal.Decimal
        Timestamp containing the Unix epoch time of the sensor in a specific frame with up to
        nanosecond precision.
    uri: str, optional
        URI to the file corresponding to the frame recording in the particular frame. Default is
        None.

    """

    sensor: Sensor
    timestamp: decimal.Decimal
    uri: str | None = None

    @classmethod
    def fromdict(cls, data_dict: dict, sensor: Sensor) -> SensorReference:
        """Generate a SensorReference object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        sensor: raillabel.format.Sensor
            Sensor corresponding to this SensorReference.

        Returns
        -------
        sensor_reference: raillabel.format.SensorReference
            Converted SensorReference object.

        """
        return SensorReference(
            sensor=sensor,
            timestamp=cls._timestamp_fromdict(data_dict["stream_properties"]),
            uri=data_dict.get("uri"),
        )

    def asdict(self) -> dict[str, Any]:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this class instance.

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.

        """
        dict_repr: dict[str, Any] = {
            "stream_properties": {"sync": {"timestamp": str(self.timestamp)}}
        }

        if self.uri is not None:
            dict_repr["uri"] = self.uri

        return dict_repr

    @classmethod
    def _timestamp_fromdict(cls, data_dict: dict) -> decimal.Decimal:
        return decimal.Decimal(data_dict["sync"]["timestamp"])
