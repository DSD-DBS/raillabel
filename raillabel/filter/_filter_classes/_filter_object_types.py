# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t

from ._filter_abc import _FilterABC, _ObjectAnnotation


class _FilterObjectTypes(_FilterABC):

    PARAMETERS = ["include_object_types", "exclude_object_types"]
    LEVELS = ["annotation"]

    def passes_filter(self, annotation: t.Type[_ObjectAnnotation]) -> bool:

        if self.include_object_types is not None:
            return annotation.object.type in self.include_object_types

        elif self.exclude_object_types is not None:
            return annotation.object.type not in self.exclude_object_types

        else:
            return True
