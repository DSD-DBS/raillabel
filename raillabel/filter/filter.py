# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from copy import deepcopy
from uuid import UUID

from raillabel.format import Bbox, Cuboid, Frame, Poly2d, Poly3d, Scene, Seg3d

from ._filter_abc import _AnnotationLevelFilter, _FilterAbc, _FrameLevelFilter


def filter_(scene: Scene, filters: list[_FilterAbc]) -> Scene:
    """Return a scene with filters applied to annotations, frame, sensors and objects."""
    filtered_scene = Scene(metadata=deepcopy(scene.metadata))

    used_sensor_ids = set()
    used_object_ids = set()

    frame_filters, annotation_filters = _separate_filters(filters)

    for frame_id, frame in scene.frames.items():
        if not _frame_passes_all_filters(frame_id, frame, frame_filters):
            continue

        filtered_frame = Frame(
            timestamp=deepcopy(frame.timestamp),
            sensors=deepcopy(frame.sensors),
            frame_data=deepcopy(frame.frame_data),
        )

        for annotation_id, annotation in frame.annotations.items():
            if not _annotation_passes_all_filters(annotation_id, annotation, annotation_filters):
                continue

            filtered_frame.annotations[annotation_id] = deepcopy(annotation)
            used_sensor_ids.add(annotation.sensor_id)
            used_object_ids.add(annotation.object_id)

        filtered_scene.frames[frame_id] = filtered_frame

    filtered_scene.sensors = {
        sensor_id: deepcopy(sensor)
        for sensor_id, sensor in scene.sensors.items()
        if sensor_id in used_sensor_ids
    }
    filtered_scene.objects = {
        object_id: deepcopy(object_)
        for object_id, object_ in scene.objects.items()
        if object_id in used_object_ids
    }

    return filtered_scene


def _separate_filters(
    all_filters: list[_FilterAbc],
) -> tuple[list[_FrameLevelFilter], list[_AnnotationLevelFilter]]:
    frame_filters = []
    annotation_filters = []
    for filter_ in all_filters:
        if isinstance(filter_, _FrameLevelFilter):
            frame_filters.append(filter_)

        if isinstance(filter_, _AnnotationLevelFilter):
            annotation_filters.append(filter_)

    return frame_filters, annotation_filters


def _frame_passes_all_filters(
    frame_id: int, frame: Frame, frame_filters: list[_FrameLevelFilter]
) -> bool:
    return all(filter_.passes_filter(frame_id, frame) for filter_ in frame_filters)


def _annotation_passes_all_filters(
    annotation_id: UUID,
    annotation: Bbox | Cuboid | Poly2d | Poly3d | Seg3d,
    annotation_filters: list[_AnnotationLevelFilter],
) -> bool:
    return all(filter_.passes_filter(annotation_id, annotation) for filter_ in annotation_filters)
