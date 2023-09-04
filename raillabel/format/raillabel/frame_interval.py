# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
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

    @classmethod
    def from_frame_uids(cls, frame_uids: t.List[int]) -> t.List["FrameInterval"]:
        """Convert a list of frame uids into FrameIntervals.

        Parameters
        ----------
        frame_uids: list[int]
            List of frame uids, that should be included in the FrameIntervals.

        Returns
        -------
        list[FrameInterval]
            FrameIntervals corresponding to the frames ids.

        Example
        -------
        FrameInterval.from_frame_uids([0, 1, 2, 3, 6, 7, 9, 12, 13, 14]) == [
            FrameInterval(0, 3),
            FrameInterval(6, 7),
            FrameInterval(9, 9),
            FrameInterval(12, 14),
        ]
        """

        sorted_frame_uids = sorted(frame_uids)
        frame_uid_intervals = cls._slice_into_intervals(sorted_frame_uids)

        frame_intervals = []
        for interval in frame_uid_intervals:
            frame_intervals.append(FrameInterval(frame_start=interval[0], frame_end=interval[-1]))

        return frame_intervals

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

    @classmethod
    def _slice_into_intervals(cls, sorted_frame_uids: t.List[int]) -> t.List[t.List[int]]:

        if len(sorted_frame_uids) == 0:
            return []

        if len(sorted_frame_uids) == 1:
            return [sorted_frame_uids]

        intervals = []
        interval_start_i = 0
        for i, frame_uid in enumerate(sorted_frame_uids[1:]):
            previous_frame_uid = sorted_frame_uids[i]

            if frame_uid - previous_frame_uid > 1:
                intervals.append(sorted_frame_uids[interval_start_i : i + 1])
                interval_start_i = i + 1

        intervals.append(sorted_frame_uids[interval_start_i : len(sorted_frame_uids)])
        interval_start_i = len(sorted_frame_uids)

        return intervals
