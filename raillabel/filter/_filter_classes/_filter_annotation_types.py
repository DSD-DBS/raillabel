# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t

from ._filter_abc import _FilterABC, _ObjectAnnotation


class _FilterAnnotationTypes(_FilterABC):

    PARAMETERS = ["include_annotation_types", "exclude_annotation_types"]
    LEVELS = ["annotation"]

    def passes_filter(self, annotation: t.Type[_ObjectAnnotation]) -> bool:

        if self.include_annotation_types is not None:
            return annotation.__class__.__name__.lower() in self.include_annotation_types

        elif self.exclude_annotation_types is not None:
            return annotation.__class__.__name__.lower() not in self.exclude_annotation_types

        else:
            return True

    def _process_filter_args(self, filter_args):
        return [arg.lower() for arg in filter_args]
