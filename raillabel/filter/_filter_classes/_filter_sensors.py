# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from typing import ClassVar

from ._filter_abc import _FilterABC, _ObjectAnnotation


class _FilterSensors(_FilterABC):
    PARAMETERS: ClassVar = ["include_sensors", "exclude_sensors"]
    LEVELS: ClassVar = ["frame_data", "annotation"]

    def passes_filter(self, annotation: t.Type[_ObjectAnnotation]) -> bool:
        if self.include_sensors is not None:
            return annotation.sensor.uid in self.include_sensors

        if self.exclude_sensors is not None:
            return annotation.sensor.uid not in self.exclude_sensors

        return True
