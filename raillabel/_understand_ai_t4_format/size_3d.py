# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Size3d:
    """Dimensional information of an object in 3d.

    Parameters
    ----------
    width: float
        Size of the object in the x-dimension.
    length: float
        Size of the object in the y-dimension.
    height: float
        Size of the object in the z-dimension.
    """

    width: float
    length: float
    height: float

    @classmethod
    def fromdict(cls, data_dict: dict) -> "Size3d":
        """Generate a Size3d from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        Size3d
            Converted 3d size.
        """

        return Size3d(
            width=float(data_dict["width"]),
            length=float(data_dict["length"]),
            height=float(data_dict["height"]),
        )
