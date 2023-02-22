# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import decimal
import typing as t
from dataclasses import dataclass

from .sensor import Sensor


@dataclass
class SensorReference:  # TODO
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
