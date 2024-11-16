# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from copy import deepcopy

from raillabel.format import Scene

from ._filter_abc import _FrameLevelFilter


def filter_(scene: Scene, filters: list[_FrameLevelFilter]) -> Scene:
    """Return a scene with filters applied to annotations, frame, sensors and objects."""
    filtered_scene = Scene(
        metadata=deepcopy(scene.metadata),
        sensors=deepcopy(scene.sensors),
        objects=deepcopy(scene.objects),
    )

    for frame_id, frame in scene.frames.items():
        frame_passes_filters = True
        for filter_ in filters:
            if not filter_.passes_filter(frame_id, frame):
                frame_passes_filters = False

        if frame_passes_filters:
            filtered_scene.frames[frame_id] = deepcopy(frame)

    return filtered_scene
