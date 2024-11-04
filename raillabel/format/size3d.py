# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Size3d:
    """The 3D size of a cube.

    Parameters
    ----------
    x: float or int
        The size along the x-axis.
    y: float or int
        The size along the y-axis.
    z: float or int
        The size along the z-axis.

    """

    x: float
    y: float
    z: float
