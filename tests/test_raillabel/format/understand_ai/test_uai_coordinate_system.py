# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

import raillabel.format.understand_ai as uai_format

# == Fixtures =========================

@pytest.fixture
def coordinate_system_camera_uai_dict(point_3d_vec, quaternion_vec) -> dict:
    return {
        "coordinate_system_id": "ir_middle",
        "topic": "/A0001781/image",
        "frame_id": " A0001781",
        "position": point_3d_vec,
        "rotation_quaternion": quaternion_vec,
        "rotation_matrix": [0] * 9,
        "angle_axis_rotation": [0] * 3,
        "homogeneous_transform": [0] * 16,
        "measured_position": [0, 0, 0],
        "camera_matrix": [
            3535,    0, 319.5,
               0, 3535, 239.5,
               0,    0,   1  ,
        ],
        "dist_coeffs": [0, 1, 2, 3, 4]
    }

@pytest.fixture
def coordinate_system_camera_uai(point_3d_vec, quaternion_vec):
    return uai_format.CoordinateSystem(
        uid="ir_middle",
        topic="/A0001781/image",
        frame_id=" A0001781",
        position=point_3d_vec,
        rotation_quaternion=quaternion_vec,
        rotation_matrix=[0] * 9,
        angle_axis_rotation=[0] * 3,
        homogeneous_transform=[0] * 16,
        measured_position=[0, 0, 0],
        camera_matrix=[
            3535,    0, 319.5,
               0, 3535, 239.5,
               0,    0,   1  ,
        ],
        dist_coeffs=[0, 1, 2, 3, 4]
    )

@pytest.fixture
def coordinate_system_camera_raillabel_dict(point_3d_vec, quaternion_vec) -> dict:
    return (
        {
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": {
                "translation": point_3d_vec,
                "quaternion": quaternion_vec
            }
        },
        {
            "type": "camera",
            "uri": "/A0001781/image",
            "stream_properties": {
                "intrinsics_pinhole": {
                    "camera_matrix": [
                        3535,    0, 319.5, 0,
                        0, 3535, 239.5, 0,
                        0,    0,   1  , 0,
                    ],
                    "distortion_coeffs": [0, 1, 2, 3, 4],
                    "width_px": 640,
                    "height_px": 480,
                }
            }
        }
    )

@pytest.fixture
def coordinate_system_camera_translated_uid() -> dict:
    return "ir_middle"


@pytest.fixture
def coordinate_system_lidar_uai_dict(point_3d_vec, quaternion_vec) -> dict:
    return {
        "coordinate_system_id": "LIDAR",
        "topic": "/lidar_merged",
        "frame_id": "lidar_merged",
        "position": point_3d_vec,
        "rotation_quaternion": quaternion_vec,
        "rotation_matrix": [0] * 9,
        "angle_axis_rotation": [0] * 3,
        "homogeneous_transform": [0] * 16,
    }

@pytest.fixture
def coordinate_system_lidar_uai(point_3d_vec, quaternion_vec):
    return uai_format.CoordinateSystem(
        uid="LIDAR",
        topic="/lidar_merged",
        frame_id="lidar_merged",
        position=point_3d_vec,
        rotation_quaternion=quaternion_vec,
        rotation_matrix=[0] * 9,
        angle_axis_rotation=[0] * 3,
        homogeneous_transform=[0] * 16,
    )

@pytest.fixture
def coordinate_system_lidar_raillabel_dict(point_3d_vec, quaternion_vec) -> dict:
    return (
        {
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": {
                "translation": point_3d_vec,
                "quaternion": quaternion_vec
            }
        },
        {
            "type": "lidar",
            "uri": "/lidar_merged",
        }
    )

@pytest.fixture
def coordinate_system_lidar_translated_uid() -> dict:
    return "lidar"


@pytest.fixture
def coordinate_system_radar_uai_dict(point_3d_vec, quaternion_vec) -> dict:
    return {
        "coordinate_system_id": "radar",
        "rotation_around_z_in_degrees": 1.22869,
        "topic": "/talker1/Nvt/Cartesian",
        "frame_id": "navtech",
        "position": point_3d_vec,
        "rotation_quaternion": quaternion_vec,
        "rotation_matrix": [0] * 9,
        "angle_axis_rotation": [0] * 3,
        "homogeneous_transform": [0] * 16,
    }

@pytest.fixture
def coordinate_system_radar_uai(point_3d_vec, quaternion_vec):
    return uai_format.CoordinateSystem(
        uid="radar",
        topic="/talker1/Nvt/Cartesian",
        frame_id="navtech",
        position=point_3d_vec,
        rotation_quaternion=quaternion_vec,
        rotation_matrix=[0] * 9,
        angle_axis_rotation=[0] * 3,
        homogeneous_transform=[0] * 16,
    )

@pytest.fixture
def coordinate_system_radar_raillabel_dict(point_3d_vec, quaternion_vec) -> dict:
    return (
        {
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": {
                "translation": point_3d_vec,
                "quaternion": quaternion_vec
            }
        },
        {
            "type": "radar",
            "uri": "/talker1/Nvt/Cartesian",
            "stream_properties": {
                "intrinsics_radar": {
                    "resolution_px_per_m": 2.856,
                    "width_px": 2856,
                    "height_px": 1428
                }
            }
        }
    )

@pytest.fixture
def coordinate_system_radar_translated_uid() -> dict:
    return "radar"

# == Tests ============================

def test_fromdict(point_3d_vec, quaternion_vec):
    coordinate_system = uai_format.CoordinateSystem.fromdict(
        {
            "coordinate_system_id": "ir_middle",
            "topic": "/A0001781/image",
            "frame_id": " A0001781",
            "position": point_3d_vec,
            "rotation_quaternion": quaternion_vec,
            "rotation_matrix": [0] * 9,
            "angle_axis_rotation": [0] * 3,
            "homogeneous_transform": [0] * 16,
            "measured_position": [0, 0, 0],
            "camera_matrix": [
                3535,    0, 319.5,
                   0, 3535, 239.5,
                   0,    0,   1  ,
            ],
            "dist_coeffs": [0, 1, 2, 3, 4]
        }
    )

    assert coordinate_system.uid == "ir_middle"
    assert coordinate_system.topic == "/A0001781/image"
    assert coordinate_system.frame_id == " A0001781"
    assert coordinate_system.position == point_3d_vec
    assert coordinate_system.rotation_quaternion == quaternion_vec
    assert coordinate_system.rotation_matrix == [0] * 9
    assert coordinate_system.angle_axis_rotation == [0] * 3
    assert coordinate_system.homogeneous_transform == [0] * 16
    assert coordinate_system.measured_position == [0, 0, 0]
    assert coordinate_system.camera_matrix == [
        3535,    0, 319.5,
           0, 3535, 239.5,
           0,    0,   1  ,
    ]
    assert coordinate_system.dist_coeffs == [0, 1, 2, 3, 4]


def test_to_raillabel__coordinate_system(point_3d_vec, quaternion_vec):
    coordinate_system = uai_format.CoordinateSystem(
        uid="ir_middle",
        topic="/A0001781/image",
        frame_id=" A0001781",
        position=point_3d_vec,
        rotation_quaternion=quaternion_vec,
        rotation_matrix=[0] * 9,
        angle_axis_rotation=[0] * 3,
        homogeneous_transform=[0] * 16,
        measured_position=[0, 0, 0],
        camera_matrix=[
            3535,    0, 319.5,
               0, 3535, 239.5,
               0,    0,   1  ,
        ],
        dist_coeffs=[0, 1, 2, 3, 4]
    )

    assert coordinate_system.to_raillabel()[0] == {
        "type": "sensor",
        "parent": "base",
        "pose_wrt_parent": {
            "translation": point_3d_vec,
            "quaternion": quaternion_vec
        }
    }

def test_to_raillabel__stream__camera(point_3d_vec, quaternion_vec):
    coordinate_system = uai_format.CoordinateSystem(
        uid="ir_middle",
        topic="/A0001781/image",
        frame_id=" A0001781",
        position=point_3d_vec,
        rotation_quaternion=quaternion_vec,
        rotation_matrix=[0] * 9,
        angle_axis_rotation=[0] * 3,
        homogeneous_transform=[0] * 16,
        measured_position=[0, 0, 0],
        camera_matrix=[
            3535,    0, 319.5,
               0, 3535, 239.5,
               0,    0,   1  ,
        ],
        dist_coeffs=[0, 1, 2, 3, 4]
    )

    assert coordinate_system.to_raillabel()[1] == {
        "type": "camera",
        "uri": "/A0001781/image",
        "stream_properties": {
            "intrinsics_pinhole": {
                "camera_matrix": [
                    3535,    0, 319.5, 0,
                       0, 3535, 239.5, 0,
                       0,    0,   1  , 0,
                ],
                "distortion_coeffs": [0, 1, 2, 3, 4],
                "width_px": 640,
                "height_px": 480,
            }
        }
    }

def test_to_raillabel__stream__lidar(point_3d_vec, quaternion_vec):
    coordinate_system = uai_format.CoordinateSystem(
        uid="LIDAR",
        topic="/lidar_merged",
        frame_id="lidar_merged",
        position=point_3d_vec,
        rotation_quaternion=quaternion_vec,
        rotation_matrix=[0] * 9,
        angle_axis_rotation=[0] * 3,
        homogeneous_transform=[0] * 16,
    )

    assert coordinate_system.to_raillabel()[1] == {
        "type": "lidar",
        "uri": "/lidar_merged",
    }

def test_to_raillabel__stream__radar(point_3d_vec, quaternion_vec):
    coordinate_system = uai_format.CoordinateSystem(
        uid="radar",
        topic="/talker1/Nvt/Cartesian",
        frame_id="navtech",
        position=point_3d_vec,
        rotation_quaternion=quaternion_vec,
        rotation_matrix=[0] * 9,
        angle_axis_rotation=[0] * 3,
        homogeneous_transform=[0] * 16,
    )

    assert coordinate_system.to_raillabel()[1] == {
        "type": "radar",
        "uri": "/talker1/Nvt/Cartesian",
        "stream_properties": {
            "intrinsics_radar": {
                "resolution_px_per_m": 2.856,
                "width_px": 2856,
                "height_px": 1428
            }
        }
    }


if __name__ == "__main__":
    import os
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
