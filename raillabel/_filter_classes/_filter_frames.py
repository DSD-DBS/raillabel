# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from ._filter_abc import Frame, _FilterABC


class _FilterFrame(_FilterABC):

    PARAMETERS = ["include_frames", "exclude_frames"]
    LEVELS = ["frame"]

    def passes_filter(self, frame: Frame) -> bool:

        if self.include_frames is not None:
            return int(frame.uid) in self.include_frames

        elif self.exclude_frames is not None:
            return int(frame.uid) not in self.exclude_frames

        else:
            return True
