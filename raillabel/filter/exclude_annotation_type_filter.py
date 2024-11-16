# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from raillabel.format import Bbox, Cuboid, Poly2d, Poly3d, Scene, Seg3d

from ._filter_abc import _AnnotationLevelFilter


@dataclass
class ExcludeAnnotationTypeFilter(_AnnotationLevelFilter):
    """Filter out all annotations in the scene, that do have the type (like bbox or cuboid)."""

    annotation_types: (
        set[Literal["bbox", "cuboid", "poly2d", "poly3d", "seg3d"]]
        | list[Literal["bbox", "cuboid", "poly2d", "poly3d", "seg3d"]]
    )

    def passes_filter(
        self, _: UUID, annotation: Bbox | Cuboid | Poly2d | Poly3d | Seg3d, __: Scene
    ) -> bool:
        """Assess if an annotation passes this filter."""
        annotation_type_str = None

        if isinstance(annotation, Bbox):
            annotation_type_str = "bbox"

        elif isinstance(annotation, Cuboid):
            annotation_type_str = "cuboid"

        elif isinstance(annotation, Poly2d):
            annotation_type_str = "poly2d"

        elif isinstance(annotation, Poly3d):
            annotation_type_str = "poly3d"

        elif isinstance(annotation, Seg3d):
            annotation_type_str = "seg3d"

        else:
            raise TypeError

        return annotation_type_str not in self.annotation_types
