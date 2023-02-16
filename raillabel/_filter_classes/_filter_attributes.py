# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t

from ._filter_abc import _Annotation, _FilterABC


class _FilterAttributes(_FilterABC):

    PARAMETERS = ["include_attributes", "exclude_attributes"]
    LEVELS = ["annotation"]

    def passes_filter(self, annotation: t.Type[_Annotation]) -> bool:

        if self.include_attributes is not None:
            for attribute_id, attribute_val in self.include_attributes.items():

                if attribute_val is None:
                    if attribute_id not in annotation.attributes:
                        return False

                else:
                    if (
                        attribute_id not in annotation.attributes
                        or annotation.attributes[attribute_id] != attribute_val
                    ):
                        return False

        elif self.exclude_attributes is not None:

            for attribute_id, attribute_val in self.exclude_attributes.items():

                if attribute_val is None:
                    if attribute_id in annotation.attributes:
                        return False

                else:
                    if (
                        attribute_id in annotation.attributes
                        and attribute_val == annotation.attributes[attribute_id]
                    ):
                        return False

        return True
