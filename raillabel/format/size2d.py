# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Size2d:
    """The size of a rectangle in a 2d image.

    Parameters
    ----------
    x: float or int
        The size along the x-axis.
    y: float or int
        The size along the y-axis.
    """

    x: float
    y: float
