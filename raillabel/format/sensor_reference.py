# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import decimal
import typing as t
from dataclasses import dataclass

from .._util._warning import _warning
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
    uri: t.Optional[str] = None

    @classmethod
    def fromdict(cls, data_dict: dict, sensor: Sensor) -> "SensorReference":
        """Generate a SensorReference object from a dictionary.

        Parameters
        ----------
        data_dict: dict
            Dict representation of the frame.
        sensor: raillabel.format.Sensor
            Sensor corresponding to this SensorReference.

        Returns
        -------
        sensor_reference: raillabel.format.SensorReference
            Converted SensorReference object.
        """

        if "stream_sync" in data_dict["stream_properties"]:
            data_dict["stream_properties"]["sync"] = data_dict["stream_properties"]["stream_sync"]
            _warning(
                "Deprecated field 'stream_sync' identified. Please update file with raillabel.save()."
            )

        sensor_reference = SensorReference(
            sensor=sensor,
            timestamp=decimal.Decimal(data_dict["stream_properties"]["sync"]["timestamp"]),
        )

        if "uri" in data_dict:
            sensor_reference.uri = data_dict["uri"]

        return sensor_reference

    def asdict(self) -> dict:
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

        dict_repr = {"stream_properties": {"sync": {"timestamp": str(self.timestamp)}}}

        if self.uri is not None:
            dict_repr["uri"] = self.uri

        return dict_repr
