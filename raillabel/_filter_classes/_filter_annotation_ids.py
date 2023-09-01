# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t

from ._filter_abc import _FilterABC, _ObjectAnnotation


class _FilterAnnotationIds(_FilterABC):

    PARAMETERS = ["include_annotation_ids", "exclude_annotation_ids"]
    LEVELS = ["annotation"]

    def passes_filter(self, annotation: t.Type[_ObjectAnnotation]) -> bool:

        if self.include_annotation_ids is not None:
            return annotation.uid in self.include_annotation_ids

        elif self.exclude_annotation_ids is not None:
            return annotation.uid not in self.exclude_annotation_ids

        else:
            return True
