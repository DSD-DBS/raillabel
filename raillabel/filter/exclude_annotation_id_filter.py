# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from raillabel.format import Bbox, Cuboid, Poly2d, Poly3d, Scene, Seg3d

from ._filter_abc import _AnnotationLevelFilter


@dataclass
class ExcludeAnnotationIdFilter(_AnnotationLevelFilter):
    """Filter out all annotations in the scene, that do have disallowed ids."""

    annotation_ids: set[UUID] | list[UUID]

    def passes_filter(
        self, annotation_id: UUID, _: Bbox | Cuboid | Poly2d | Poly3d | Seg3d, __: Scene
    ) -> bool:
        """Assess if an annotation passes this filter."""
        return annotation_id not in self.annotation_ids
