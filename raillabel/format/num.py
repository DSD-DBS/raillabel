# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from .sensor import Sensor


@dataclass
class Num:
    """A number.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier of the annotation.
    name: str
        Human readable name describing the annotation.
    val: int or float
        This is the value of the number object.
    attributes: dict, optional
        Attributes of the annotation. Dict keys are the uid str of the attribute, values are the
        attribute values. Default is {}.
    sensor: raillabel.format.Sensor
        A reference to the sensor, this value is represented in. Default is None.

    """

    uid: str
    name: str
    val: int | float
    sensor: Sensor
