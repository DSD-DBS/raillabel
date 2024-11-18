# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from raillabel.format import Frame

from ._filter_abc import _FrameLevelFilter


@dataclass
class EndTimeFilter(_FrameLevelFilter):
    """Filter out all the frames in the scene with timestamps higher than the end_time."""

    end_time: float | Decimal

    def passes_filter(self, _: int, frame: Frame) -> bool:
        """Assess if a frame passes this filter."""
        if frame.timestamp is not None:
            return frame.timestamp <= self.end_time

        return True
