# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from decimal import Decimal
from typing import ClassVar

from ._filter_abc import Frame, _FilterABC


class _FilterEnd(_FilterABC):
    PARAMETERS: ClassVar = ["end_frame", "end_timestamp"]
    LEVELS: ClassVar = ["frame"]

    def passes_filter(self, frame: Frame) -> bool:
        if self.end_frame is not None:
            return frame.uid <= self.end_frame

        if self.end_timestamp is not None:
            return frame.timestamp <= Decimal(self.end_timestamp)

        return True
