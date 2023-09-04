# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from decimal import Decimal

from ._filter_abc import Frame, _FilterABC


class _FilterEnd(_FilterABC):

    PARAMETERS = ["end_frame", "end_timestamp"]
    LEVELS = ["frame"]

    def passes_filter(self, frame: Frame) -> bool:

        if self.end_frame is not None:
            return frame.uid <= self.end_frame

        elif self.end_timestamp is not None:
            return frame.timestamp <= Decimal(self.end_timestamp)

        else:
            return True
