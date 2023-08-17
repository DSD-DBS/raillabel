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

def test_fromdict_lidar(json_data):
    input_data = json_data["_understand_ai_t4_format/coordinate_system_lidar"]
    coordinate_system = uai_format.CoordinateSystem.fromdict(input_data)

    assert coordinate_system.uid == input_data["coordinate_system_id"]
    assert coordinate_system.topic == input_data["topic"]
    assert coordinate_system.frame_id == input_data["frame_id"]
    assert coordinate_system.position == input_data["position"]
    assert coordinate_system.rotation_quaternion == input_data["rotation_quaternion"]
    assert coordinate_system.rotation_matrix == input_data["rotation_matrix"]
    assert coordinate_system.angle_axis_rotation == input_data["angle_axis_rotation"]
    assert coordinate_system.homogeneous_transform == input_data["homogeneous_transform"]
    assert coordinate_system.measured_position == None
    assert coordinate_system.camera_matrix == None
    assert coordinate_system.dist_coeffs == None

def test_to_raillabel_camera(json_data):
    input_data = json_data["_understand_ai_t4_format/coordinate_system_camera"]
    coordinate_system = uai_format.CoordinateSystem.fromdict(input_data)
    output_cs, output_stream = coordinate_system.to_raillabel()
    ground_truth_cs = json_data["_understand_ai_t4_format/coordinate_system_camera_cs_raillabel"]
    ground_truth_stream = json_data["_understand_ai_t4_format/coordinate_system_camera_stream_raillabel"]

    assert output_cs == ground_truth_cs
    assert output_stream == ground_truth_stream

def test_to_raillabel_lidar(json_data):
    input_data = json_data["_understand_ai_t4_format/coordinate_system_lidar"]
    coordinate_system = uai_format.CoordinateSystem.fromdict(input_data)
    _, output_stream = coordinate_system.to_raillabel()
    ground_truth_stream = json_data["_understand_ai_t4_format/coordinate_system_lidar_stream_raillabel"]

    assert output_stream == ground_truth_stream

def test_to_raillabel_radar(json_data):
    input_data = json_data["_understand_ai_t4_format/coordinate_system_radar"]
    coordinate_system = uai_format.CoordinateSystem.fromdict(input_data)
    _, output_stream = coordinate_system.to_raillabel()
    ground_truth_stream = json_data["_understand_ai_t4_format/coordinate_system_radar_stream_raillabel"]

    assert output_stream == ground_truth_stream

# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
