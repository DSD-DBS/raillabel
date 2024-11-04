# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import decimal
from dataclasses import dataclass

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
