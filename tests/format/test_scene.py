# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from uuid import UUID

import pytest

from raillabel.format import Scene
from raillabel.scene_builder import SceneBuilder
from raillabel.json_format import (
    JSONScene,
    JSONSceneContent,
    JSONCoordinateSystem,
    JSONFrameInterval,
)

# == Fixtures =========================


@pytest.fixture
def scene_json(
    metadata_json,
    camera_json,
    lidar_json,
    radar_json,
    object_person_id,
    object_person_json,
    object_track_id,
    object_track_json,
    frame_json,
) -> JSONScene:
    return JSONScene(
        openlabel=JSONSceneContent(
            metadata=metadata_json,
            coordinate_systems={
                "base": JSONCoordinateSystem(
                    parent="",
                    type="local",
                    pose_wrt_parent=None,
                    children=["rgb_center", "lidar", "radar"],
                ),
                "rgb_center": camera_json[1],
                "lidar": lidar_json[1],
                "radar": radar_json[1],
            },
            streams={
                "rgb_center": camera_json[0],
                "lidar": lidar_json[0],
                "radar": radar_json[0],
            },
            objects={
                object_person_id: object_person_json,
                object_track_id: object_track_json,
            },
            frames={1: frame_json},
            frame_intervals=[JSONFrameInterval(frame_start=1, frame_end=1)],
        )
    )


@pytest.fixture
def scene(
    metadata,
    camera,
    lidar,
    radar,
    object_person_id,
    object_person,
    object_track_id,
    object_track,
    frame,
) -> Scene:
    return Scene(
        metadata=metadata,
        sensors={
            "rgb_center": camera,
            "lidar": lidar,
            "radar": radar,
        },
        objects={
            object_person_id: object_person,
            object_track_id: object_track,
        },
        frames={1: frame},
    )


# == Tests ============================


def test_from_json(scene, scene_json):
    actual = Scene.from_json(scene_json)
    assert actual == scene


def test_to_json(scene, scene_json):
    actual = scene.to_json()
    assert actual == scene_json


def test_annotations_with_frame_id(bbox, cuboid, poly2d):
    scene = (
        SceneBuilder.empty()
        .add_annotation(bbox, uid="1dbe924e-23f1-4313-9524-33ef9647160d", frame_id=1)
        .add_annotation(cuboid, uid="cfebad9d-8fca-4a21-be7a-0555ff1fe4d2", frame_id=1)
        .add_annotation(poly2d, uid="66137a24-634f-4d5f-837c-ebe9a53859b5", frame_id=2)
        .result
    )

    assert scene.annotations() == {
        UUID("1dbe924e-23f1-4313-9524-33ef9647160d"): bbox,
        UUID("cfebad9d-8fca-4a21-be7a-0555ff1fe4d2"): cuboid,
        UUID("66137a24-634f-4d5f-837c-ebe9a53859b5"): poly2d,
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
