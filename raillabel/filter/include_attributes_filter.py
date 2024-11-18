# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from raillabel.format import Bbox, Cuboid, Poly2d, Poly3d, Scene, Seg3d

from ._filter_abc import _AnnotationLevelFilter


@dataclass
class IncludeAttributesFilter(_AnnotationLevelFilter):
    """Filter out all annotations in the scene, that do NOT have matching attributes.

    If an attribute has None as the value, all annotations are excluded, that do not have this
    attribute. If the value is anything other than None, all annotations are excluded that do not
    have the attribute or where the value does not match.
    """

    attributes: dict[str, bool | float | str | list | None]

    def passes_filter(
        self, _: UUID, annotation: Bbox | Cuboid | Poly2d | Poly3d | Seg3d, __: Scene
    ) -> bool:
        """Assess if an annotation passes this filter."""
        for attribute_name, attribute_value in annotation.attributes.items():
            if attribute_name not in self.attributes:
                return False

            if (
                self.attributes[attribute_name] is not None
                and attribute_value != self.attributes[attribute_name]
            ):
                return False

        return True