# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from typing import ClassVar

from ._filter_abc import Frame, _FilterABC


class _FilterFrame(_FilterABC):
    PARAMETERS: ClassVar = ["include_frames", "exclude_frames"]
    LEVELS: ClassVar = ["frame"]

    def passes_filter(self, frame: Frame) -> bool:
        if self.include_frames is not None:
            return int(frame.uid) in self.include_frames

        if self.exclude_frames is not None:
            return int(frame.uid) not in self.exclude_frames

        return True
