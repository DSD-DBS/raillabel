# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from typing import ClassVar

from ._filter_abc import _FilterABC, _ObjectAnnotation


class _FilterObjectTypes(_FilterABC):
    PARAMETERS: ClassVar = ["include_object_types", "exclude_object_types"]
    LEVELS: ClassVar = ["annotation"]

    def passes_filter(self, annotation: t.Type[_ObjectAnnotation]) -> bool:
        if self.include_object_types is not None:
            return annotation.object.type in self.include_object_types

        if self.exclude_object_types is not None:
            return annotation.object.type not in self.exclude_object_types

        return True
