# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

import raillabel.format.understand_ai as uai_format
from raillabel._util._warning import _WarningsLogger

# == Fixtures =========================

@pytest.fixture
def scene_uai_dict(
    metadata_uai_dict,
    coordinate_system_camera_uai_dict,
    coordinate_system_lidar_uai_dict,
    coordinate_system_radar_uai_dict,
    frame_uai_dict,
) -> dict:
    return {
        "metadata": metadata_uai_dict,
        "coordinateSystems": [
            coordinate_system_camera_uai_dict,
            coordinate_system_lidar_uai_dict,
            coordinate_system_radar_uai_dict,
        ],
        "frames": [frame_uai_dict]
    }

@pytest.fixture
def scene_uai(
    metadata_uai,
    coordinate_system_camera_uai,
    coordinate_system_lidar_uai,
    coordinate_system_radar_uai,
    frame_uai,
):
    return uai_format.Scene(
        metadata=metadata_uai,
        coordinate_systems={
            coordinate_system_camera_uai.uid: coordinate_system_camera_uai,
            coordinate_system_lidar_uai.uid: coordinate_system_lidar_uai,
            coordinate_system_radar_uai.uid: coordinate_system_radar_uai,
        },
        frames={
            frame_uai.id: frame_uai
        },
    )

@pytest.fixture
def scene_raillabel_dict(
    metadata_raillabel_dict,
    coordinate_system_camera_uai, coordinate_system_camera_raillabel_dict,
    coordinate_system_lidar_uai, coordinate_system_lidar_raillabel_dict,
    coordinate_system_radar_uai, coordinate_system_radar_raillabel_dict,
) -> dict:
    return

# == Tests ============================

def test_fromdict(
    metadata_uai_dict, metadata_uai,
    coordinate_system_camera_uai_dict, coordinate_system_camera_uai,
    coordinate_system_lidar_uai_dict, coordinate_system_lidar_uai,
    coordinate_system_radar_uai_dict, coordinate_system_radar_uai,
    frame_uai_dict, frame_uai,
):
    scene = uai_format.Scene.fromdict(
        {
            "metadata": metadata_uai_dict,
            "coordinateSystems": [
                coordinate_system_camera_uai_dict,
                coordinate_system_lidar_uai_dict,
                coordinate_system_radar_uai_dict,
            ],
            "frames": [frame_uai_dict]
        }
    )

    assert scene.metadata == metadata_uai
    assert scene.coordinate_systems == {
        coordinate_system_camera_uai.uid: coordinate_system_camera_uai,
        coordinate_system_lidar_uai.uid: coordinate_system_lidar_uai,
        coordinate_system_radar_uai.uid: coordinate_system_radar_uai,
    }
    assert scene.frames == {
        frame_uai.id: frame_uai
    }

def test_fromdict_duplicate_frame_id_warning(
    metadata_uai_dict,
    coordinate_system_camera_uai_dict,
    coordinate_system_lidar_uai_dict,
    coordinate_system_radar_uai_dict,
    frame_uai_dict,
):
    with _WarningsLogger() as logger:
        scene = uai_format.Scene.fromdict(
            {
                "metadata": metadata_uai_dict,
                "coordinateSystems": [
                    coordinate_system_camera_uai_dict,
                    coordinate_system_lidar_uai_dict,
                    coordinate_system_radar_uai_dict,
                ],
                "frames": [frame_uai_dict, frame_uai_dict]
            }
        )

    assert len(logger.warnings) == 1
    assert "0" in logger.warnings[0]
    assert len(scene.frames) == 1


def test_to_raillabel__metadata(metadata_uai, metadata_raillabel_dict):
    scene = uai_format.Scene(
        metadata=metadata_uai,
        coordinate_systems={},
        frames={},
    )

    assert scene.to_raillabel()["openlabel"]["metadata"] == metadata_raillabel_dict

def test_to_raillabel__sensors(
    metadata_uai,
    coordinate_system_camera_uai, coordinate_system_lidar_uai,
    coordinate_system_camera_raillabel_dict, coordinate_system_lidar_raillabel_dict,
    coordinate_system_camera_translated_uid, coordinate_system_lidar_translated_uid,
):
    scene = uai_format.Scene(
        metadata=metadata_uai,
        coordinate_systems={
            coordinate_system_camera_uai.uid: coordinate_system_camera_uai,
            coordinate_system_lidar_uai.uid: coordinate_system_lidar_uai,
        },
        frames={},
    )

    assert scene.to_raillabel()["openlabel"]["coordinate_systems"] == {
        "base": {
            "type": "local",
            "parent": "",
            "children": [
                coordinate_system_camera_translated_uid,
                coordinate_system_lidar_translated_uid
            ]
        },
        coordinate_system_camera_translated_uid: coordinate_system_camera_raillabel_dict[0],
        coordinate_system_lidar_translated_uid: coordinate_system_lidar_raillabel_dict[0],
    }
    assert scene.to_raillabel()["openlabel"]["streams"] == {
        coordinate_system_camera_translated_uid: coordinate_system_camera_raillabel_dict[1],
        coordinate_system_lidar_translated_uid: coordinate_system_lidar_raillabel_dict[1],
    }

def test_to_raillabel__frames(
    metadata_uai,
    coordinate_system_camera_uai, coordinate_system_lidar_uai,
    frame_uai, frame_raillabel_dict
):
    scene = uai_format.Scene(
        metadata=metadata_uai,
        coordinate_systems={
            coordinate_system_camera_uai.uid: coordinate_system_camera_uai,
            coordinate_system_lidar_uai.uid: coordinate_system_lidar_uai,
        },
        frames={
            frame_uai.id: frame_uai
        },
    )

    assert scene.to_raillabel()["openlabel"]["frames"] == {
        str(frame_uai.id): frame_raillabel_dict
    }


if __name__ == "__main__":
    import os
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-vv"])
