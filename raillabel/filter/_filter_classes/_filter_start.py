# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from decimal import Decimal

from ._filter_abc import Frame, _FilterABC


class _FilterStart(_FilterABC):

    PARAMETERS = ["start_frame", "start_timestamp"]
    LEVELS = ["frame"]

    def passes_filter(self, frame: Frame) -> bool:

        if self.start_frame is not None:
            return frame.uid >= self.start_frame

        elif self.start_timestamp is not None:
            return frame.timestamp >= Decimal(self.start_timestamp)

        else:
            return True
