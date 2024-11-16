# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from raillabel.format import Bbox, Cuboid, Poly2d, Poly3d, Scene, Seg3d

from ._filter_abc import _AnnotationLevelFilter


@dataclass
class ExcludeObjectTypeFilter(_AnnotationLevelFilter):
    """Filter out all annotations in the scene, that do match the type (like 'person')."""

    object_types: list[str]

    def passes_filter(
        self, _: UUID, annotation: Bbox | Cuboid | Poly2d | Poly3d | Seg3d, scene: Scene
    ) -> bool:
        """Assess if an annotation passes this filter."""
        return scene.objects[annotation.object_id].type not in self.object_types
