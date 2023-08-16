# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class IntrinsicsRadar:
    """Intrinsic calibration for a radar sensor.

    Parameters
    ----------
    resolution_px_per_m: float
        Factor for calculating the 3D coordinates of a pixel in the cartesian radar images.
        Number of pixels in the images per meter from the sensor.
    width_px: int
        Width of the cartesian image frame in pixels.
    height_px: int
        Height of the cartesian image frame in pixels.
    """

    resolution_px_per_m: float
    width_px: int
    height_px: int

    @classmethod
    def fromdict(cls, data_dict: dict) -> "IntrinsicsRadar":
        """Generate a IntrinsicsRadar object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.

        Returns
        -------
        raillabel.format.IntrinsicsRadar
            Converted IntrinsicsRadar object.
        """

        return IntrinsicsRadar(
            resolution_px_per_m=data_dict["resolution_px_per_m"],
            width_px=data_dict["width_px"],
            height_px=data_dict["height_px"],
        )

    def asdict(self) -> dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict
            Dict representation of this class instance.

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.
        """

        return {
            "resolution_px_per_m": float(self.resolution_px_per_m),
            "width_px": int(self.width_px),
            "height_px": int(self.height_px),
        }
