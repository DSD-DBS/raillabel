# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class FrameInterval:
    """Closed interval of frames.

    Parameters
    ----------
    frame_start: int
        Initial frame number of the interval (inclusive).
    frame_end: int
        Ending frame number of the interval (inclusive).
    """

    frame_start: int
    frame_end: int

    @classmethod
    def fromdict(cls, data_dict: dict) -> "FrameInterval":
        """Generate a FrameInterval object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        """

        return FrameInterval(
            frame_start=data_dict["frame_start"],
            frame_end=data_dict["frame_end"],
        )

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

        return {
            "frame_start": int(self.frame_start),
            "frame_end": int(self.frame_end),
        }

    def __len__(self) -> int:
        """Return the length in frames."""
        return abs(self.frame_start - self.frame_end) + 1
