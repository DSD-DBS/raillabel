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
    def from_frame_ids(cls, frame_ids: list[int]) -> list[FrameInterval]:
        """Convert a list of frame uids into FrameIntervals.

        Example:
        .. code-block:: python

            FrameInterval.from_frame_ids([0, 1, 2, 3, 9, 12, 13, 14]) == [
                FrameInterval(0, 3),
                FrameInterval(9, 9),
                FrameInterval(12, 14),
            ]
        """
        sorted_frame_ids = sorted(frame_ids)
        frame_id_intervals = _slice_into_intervals(sorted_frame_ids)

        return [
            FrameInterval(start=interval[0], end=interval[-1]) for interval in frame_id_intervals
        ]

    def to_json(self) -> JSONFrameInterval:
        """Export this object into the RailLabel JSON format."""
        return JSONFrameInterval(
            frame_start=self.start,
            frame_end=self.end,
        )

    def __len__(self) -> int:
        """Return the length in frames."""
        return abs(self.start - self.end) + 1


def _slice_into_intervals(sorted_frame_ids: list[int]) -> list[list[int]]:
    if len(sorted_frame_ids) == 0:
        return []

    if len(sorted_frame_ids) == 1:
        return [sorted_frame_ids]

    intervals = []
    interval_start_i = 0
    for i, frame_id in enumerate(sorted_frame_ids[1:]):
        previous_frame_id = sorted_frame_ids[i]

        if frame_id - previous_frame_id > 1:
            intervals.append(sorted_frame_ids[interval_start_i : i + 1])
            interval_start_i = i + 1

    intervals.append(sorted_frame_ids[interval_start_i : len(sorted_frame_ids)])
    interval_start_i = len(sorted_frame_ids)

    return intervals
