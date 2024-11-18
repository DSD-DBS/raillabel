# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from raillabel.format import Bbox, Cuboid, Poly2d, Poly3d, Scene, Seg3d

from ._filter_abc import _AnnotationLevelFilter


@dataclass
class IncludeSensorTypeFilter(_AnnotationLevelFilter):
    """Filter out all annotations in the scene, that do NOT match the sensor type (like 'camera')."""

    sensor_types: list[Literal["camera", "lidar", "radar", "gps_imu", "other"]]

    def passes_filter(
        self, _: UUID, annotation: Bbox | Cuboid | Poly2d | Poly3d | Seg3d, scene: Scene
    ) -> bool:
        """Assess if an annotation passes this filter."""
        return scene.sensors[annotation.sensor_id].TYPE in self.sensor_types
