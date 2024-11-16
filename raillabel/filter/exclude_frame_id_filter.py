# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.format import Frame

from ._filter_abc import _FrameLevelFilter


@dataclass
class ExcludeFrameIdFilter(_FrameLevelFilter):
    """Filter out all the frames in the scene that do match a list of disallowed ids."""

    frame_ids: set[int] | list[int]

    def passes_filter(self, frame_id: int, _: Frame) -> bool:
        """Assess if a frame passes this filter."""
        return frame_id not in self.frame_ids