# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel
import raillabel._understand_ai_t4_format as uai_format


def test_fromdict_camera():
    coordinate_system = uai_format.CoordinateSystem.fromdict({
        "coordinate_system_id": "rgb_middle_rect",
        "topic": "/S1206063/image",
        "frame_id": "S1206063",
        "position": [0.0669458, -0.000911152, 2.05432],
        "rotation_quaternion": [0.99999, 0.00193374, -0.00293566, 0.00271082],
        "rotation_matrix": [
            0.9999680667369587,  -0.005432933661727504, -0.005860779656024867,
            0.005410226430795589, 0.9999778242364062,   -0.003883360064516633,
            0.005881747726375861, 0.003851527911158113,  0.9999752850828029
        ],
        "angle_axis_rotation": [0.00386749, -0.00587134, 0.00542165],
        "homogeneous_transform": [
            0.9999680667369587,  -0.005432933661727504, -0.005860779656024867,  0.06694577073389593,
            0.005410226430795589, 0.9999778242364062,   -0.003883360064516633, -0.0009111521949818156,
            0.005881747726375861, 0.003851527911158113,  0.9999752850828029,    2.054322280217477,
            0,                    0,                     0,                     1
        ],
        "measured_position": [0, 0, 0],
        "camera_matrix": [
            4609.471892628096, 0,                 1257.158605934,
            0,                 4609.471892628096, 820.0498076210201,
            0,                 0,                 1
        ],
        "dist_coeffs": [-0.0914603, 0.605326, 0, 0, 0.417134]
    })

    assert coordinate_system.uid == "rgb_middle_rect"
    assert coordinate_system.topic == "/S1206063/image"
    assert coordinate_system.frame_id == "S1206063"
    assert coordinate_system.position == [0.0669458, -0.000911152, 2.05432]
    assert coordinate_system.rotation_quaternion == [0.99999, 0.00193374, -0.00293566, 0.00271082]
    assert coordinate_system.rotation_matrix == [
        0.9999680667369587,  -0.005432933661727504, -0.005860779656024867,
        0.005410226430795589, 0.9999778242364062,   -0.003883360064516633,
        0.005881747726375861, 0.003851527911158113,  0.9999752850828029
    ]
    assert coordinate_system.angle_axis_rotation == [0.00386749, -0.00587134, 0.00542165]
    assert coordinate_system.homogeneous_transform == [
        0.9999680667369587,  -0.005432933661727504, -0.005860779656024867,  0.06694577073389593,
        0.005410226430795589, 0.9999778242364062,   -0.003883360064516633, -0.0009111521949818156,
        0.005881747726375861, 0.003851527911158113,  0.9999752850828029,    2.054322280217477,
        0,                    0,                     0,                     1
    ]
    assert coordinate_system.measured_position == [0, 0, 0]
    assert coordinate_system.camera_matrix == [
        4609.471892628096, 0,                 1257.158605934,
        0,                 4609.471892628096, 820.0498076210201,
        0,                 0,                 1
    ]
    assert coordinate_system.dist_coeffs == [-0.0914603, 0.605326, 0, 0, 0.417134]


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
