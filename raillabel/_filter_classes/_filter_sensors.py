# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t

from ._filter_abc import _Annotation, _FilterABC


class _FilterSensors(_FilterABC):

    PARAMETERS = ["include_sensors", "exclude_sensors"]
    LEVELS = ["frame_data", "annotation"]

    def passes_filter(self, annotation: t.Type[_Annotation]) -> bool:

        if self.include_sensors is not None:
            return annotation.sensor.uid in self.include_sensors

        elif self.exclude_sensors is not None:
            return annotation.sensor.uid not in self.exclude_sensors

        else:
            return True
