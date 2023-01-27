# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass


@dataclass
class Quaternion:
    """A quaternion.

    Parameters
    ----------
    x: float or int
        The x component of the quaternion.
    y: float or int
        The y component of the quaternion.
    z: float or int
        The z component of the quaternion.
    w: float or int
        The w component of the quaternion.
    """

    x: t.Union[float, int]
    y: t.Union[float, int]
    z: t.Union[float, int]
    w: t.Union[float, int]
