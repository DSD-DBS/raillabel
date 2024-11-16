# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.format import Frame

from ._filter_abc import _FrameLevelFilter


@dataclass
class FrameIdFilter(_FrameLevelFilter):
    """Filter for the frames in a scene based on the frame id."""

    include_frame_ids: set[int] | None = None

    def passes_filter(self, frame_id: int, _: Frame) -> bool:
        """Assess if a frame passes this filter."""
        if self.include_frame_ids is None:
            return True

        if frame_id in self.include_frame_ids:
            return True

        return False
