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

        return [float(self.x), float(self.y)]
