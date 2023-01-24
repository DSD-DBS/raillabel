# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass
from typing import Union


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

    x: Union[float, int]
    y: Union[float, int]
    z: Union[float, int]
    w: Union[float, int]
