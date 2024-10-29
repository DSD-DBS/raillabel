# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from decimal import Decimal
from typing import ClassVar

from ._filter_abc import Frame, _FilterABC


class _FilterStart(_FilterABC):
    PARAMETERS: ClassVar = ["start_frame", "start_timestamp"]
    LEVELS: ClassVar = ["frame"]

    def passes_filter(self, frame: Frame) -> bool:
        if self.start_frame is not None:
            return frame.uid >= self.start_frame

        if self.start_timestamp is not None:
            return frame.timestamp >= Decimal(self.start_timestamp)

        return True
