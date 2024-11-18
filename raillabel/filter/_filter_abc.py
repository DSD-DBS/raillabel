# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from raillabel.format import Bbox, Cuboid, Frame, Poly2d, Poly3d, Scene, Seg3d


class _FilterAbc(ABC):
    """Base class of all filter classes regardless of level."""


class _AnnotationLevelFilter(_FilterAbc):
    """Base class of all filter classes applied to the annotations."""

    @abstractmethod
    def passes_filter(
        self, annotation_id: UUID, annotation: Bbox | Cuboid | Poly2d | Poly3d | Seg3d, scene: Scene
    ) -> bool:
        """Assess if an annotation passes this filter."""
        raise NotImplementedError


class _FrameLevelFilter(_FilterAbc):
    """Base class of all filter classes applied to the frames."""

    @abstractmethod
    def passes_filter(self, frame_id: int, frame: Frame) -> bool:
        """Assess if a frame passes this filter."""
        raise NotImplementedError
