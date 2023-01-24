# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Point2d:
    """A 2d point in an image.

    Parameters
    ----------
    x: float or int
        The x-coordinate of the point in the image.
    y: float or int
        The y-coordinate of the point in the image.
    """

    x: float
    y: float
