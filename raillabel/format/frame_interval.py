# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.json_format import JSONFrameInterval


@dataclass
class FrameInterval:
    """Closed interval of frames."""

    start: int
    "Initial frame number of the interval (inclusive)."

    end: int
    "Ending frame number of the interval (inclusive)."

    @classmethod
    def from_json(cls, json: JSONFrameInterval) -> FrameInterval:
        """Construct an instant of this class from RailLabel JSON data."""
        return FrameInterval(
            start=json.frame_start,
            end=json.frame_end,
        )

    @classmethod
    def fromdict(cls, data_dict: dict) -> FrameInterval:
        """Generate a FrameInterval object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.

        """
        return FrameInterval(
            start=data_dict["frame_start"],
            end=data_dict["frame_end"],
        )

    @classmethod
    def from_frame_uids(cls, frame_uids: list[int]) -> list[FrameInterval]:
        """Convert a list of frame uids into FrameIntervals.

        Example:
        -------
        ```python
        FrameInterval.from_frame_uids([0, 1, 2, 3, 9, 12, 13, 14]) == [
            FrameInterval(0, 3),
            FrameInterval(9, 9),
            FrameInterval(12, 14),
        ]
        ```

        """
        sorted_frame_uids = sorted(frame_uids)
        frame_uid_intervals = cls._slice_into_intervals(sorted_frame_uids)

        return [
            FrameInterval(start=interval[0], end=interval[-1]) for interval in frame_uid_intervals
        ]

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
            "frame_start": int(self.start),
            "frame_end": int(self.end),
        }

    def __len__(self) -> int:
        """Return the length in frames."""
        return abs(self.start - self.end) + 1

    @classmethod
    def _slice_into_intervals(cls, sorted_frame_uids: list[int]) -> list[list[int]]:
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
