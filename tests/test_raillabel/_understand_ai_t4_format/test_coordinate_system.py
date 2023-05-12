# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel._understand_ai_t4_format as uai_format


def test_fromdict_camera(json_data):
    input_data = json_data["_understand_ai_t4_format/coordinate_system_camera"]
    coordinate_system = uai_format.CoordinateSystem.fromdict(input_data)

    assert coordinate_system.uid == input_data["coordinate_system_id"]
    assert coordinate_system.topic == input_data["topic"]
    assert coordinate_system.frame_id == input_data["frame_id"]
    assert coordinate_system.position == input_data["position"]
    assert coordinate_system.rotation_quaternion == input_data["rotation_quaternion"]
    assert coordinate_system.rotation_matrix == input_data["rotation_matrix"]
    assert coordinate_system.angle_axis_rotation == input_data["angle_axis_rotation"]
    assert coordinate_system.homogeneous_transform == input_data["homogeneous_transform"]
    assert coordinate_system.measured_position == input_data["measured_position"]
    assert coordinate_system.camera_matrix == input_data["camera_matrix"]
    assert coordinate_system.dist_coeffs == input_data["dist_coeffs"]


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
