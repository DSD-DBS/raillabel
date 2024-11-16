# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from copy import deepcopy
from uuid import UUID

from raillabel.format import (
    Bbox,
    Camera,
    Cuboid,
    Frame,
    GpsImu,
    Lidar,
    Object,
    OtherSensor,
    Poly2d,
    Poly3d,
    Radar,
    Scene,
    Seg3d,
)

from ._filter_abc import _AnnotationLevelFilter, _FilterAbc, _FrameLevelFilter


def filter_(scene: Scene, filters: list[_FilterAbc]) -> Scene:
    """Return a scene with filters applied to annotations, frame, sensors and objects."""
    frame_filters, annotation_filters = _separate_filters(filters)

    filtered_scene = Scene(metadata=deepcopy(scene.metadata))
    filtered_scene.frames = _filter_frames(scene.frames, frame_filters, annotation_filters)
    filtered_scene.sensors = _get_used_sensors(scene, filtered_scene)
    filtered_scene.objects = _get_used_objects(scene, filtered_scene)

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


def _filter_frames(
    frames: dict[int, Frame],
    frame_filters: list[_FrameLevelFilter],
    annotation_filters: list[_AnnotationLevelFilter],
) -> dict[int, Frame]:
    filtered_frames = {}

    for frame_id, frame in frames.items():
        if _frame_passes_all_filters(frame_id, frame, frame_filters):
            filtered_frames[frame_id] = Frame(
                timestamp=deepcopy(frame.timestamp),
                sensors=deepcopy(frame.sensors),
                frame_data=deepcopy(frame.frame_data),
                annotations=_filter_annotations(frame, annotation_filters),
            )

    return filtered_frames


def _filter_annotations(
    frame: Frame, annotation_filters: list[_AnnotationLevelFilter]
) -> dict[UUID, Bbox | Cuboid | Poly2d | Poly3d | Seg3d]:
    annotations = {}

    for annotation_id, annotation in frame.annotations.items():
        if _annotation_passes_all_filters(annotation_id, annotation, annotation_filters):
            annotations[annotation_id] = deepcopy(annotation)

    return annotations


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


def _get_used_sensors(
    scene: Scene, filtered_scene: Scene
) -> dict[str, Camera | Lidar | Radar | GpsImu | OtherSensor]:
    used_sensors = {}
    for frame in filtered_scene.frames.values():
        for annotation in frame.annotations.values():
            if annotation.sensor_id not in used_sensors:
                used_sensors[annotation.sensor_id] = deepcopy(scene.sensors[annotation.sensor_id])

    return used_sensors


def _get_used_objects(scene: Scene, filtered_scene: Scene) -> dict[UUID, Object]:
    used_objects = {}
    for frame in filtered_scene.frames.values():
        for annotation in frame.annotations.values():
            if annotation.object_id not in used_objects:
                used_objects[annotation.object_id] = deepcopy(scene.objects[annotation.object_id])

    return used_objects
