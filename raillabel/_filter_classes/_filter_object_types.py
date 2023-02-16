# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t

from ._filter_abc import _Annotation, _FilterABC


class _FilterObjectTypes(_FilterABC):

    PARAMETERS = ["include_object_types", "exclude_object_types"]
    LEVELS = ["object"]

    def passes_filter(self, object: t.Type[_Annotation]) -> bool:

        if self.include_object_types is not None:
            return object.type in self.include_object_types

        elif self.exclude_object_types is not None:
            return object.type not in self.exclude_object_types

        else:
            return True
