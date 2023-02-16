# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t

from ._filter_abc import _Annotation, _FilterABC


class _FilterObjectIds(_FilterABC):

    PARAMETERS = ["include_object_ids", "exclude_object_ids"]
    LEVELS = ["object"]

    def passes_filter(self, object: t.Type[_Annotation]) -> bool:

        if self.include_object_ids is not None:
            return object.uid in self.include_object_ids

        elif self.exclude_object_ids is not None:
            return object.uid not in self.exclude_object_ids

        else:
            return True
