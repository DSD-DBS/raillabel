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

        dict_repr = {
            "frame_start": int(self.frame_start),
            "frame_end": int(self.frame_end),
        }

        return dict_repr

    def __len__(self) -> int:
        """Return the length in frames."""
        return abs(self.frame_start - self.frame_end) + 1
