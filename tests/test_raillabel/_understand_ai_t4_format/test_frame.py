# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel._understand_ai_t4_format as uai_format


def _prepare_frame_data(frame_data: dict, json_data: dict) -> dict:
    frame_data["annotations"]["2D_BOUNDING_BOX"] = [json_data["_understand_ai_t4_format/bounding_box_2d"]]
    frame_data["annotations"]["2D_BOUNDING_BOX"][0]["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_camera"]
    frame_data["annotations"]["2D_POLYLINE"] = [json_data["_understand_ai_t4_format/polyline_2d"]]
    frame_data["annotations"]["2D_POLYLINE"][0]["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_camera"]
    frame_data["annotations"]["2D_POLYGON"] = [json_data["_understand_ai_t4_format/polygon_2d"]]
    frame_data["annotations"]["2D_POLYGON"][0]["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_camera"]
    frame_data["annotations"]["3D_BOUNDING_BOX"] = [json_data["_understand_ai_t4_format/bounding_box_3d"]]
    frame_data["annotations"]["3D_BOUNDING_BOX"][0]["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_lidar"]
    frame_data["annotations"]["3D_SEGMENTATION"] = [json_data["_understand_ai_t4_format/segmentation_3d"]]
    frame_data["annotations"]["3D_SEGMENTATION"][0]["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_lidar"]

    return frame_data


def test_fromdict(json_data):
    input_data = _prepare_frame_data(json_data["_understand_ai_t4_format/frame"], json_data)
    frame = uai_format.Frame.fromdict(input_data)

    assert frame.id == int(input_data["frameId"])
    assert frame.timestamp == Decimal(input_data["timestamp"])
    assert len(frame.annotations) == 5
    assert frame.annotations[json_data["_understand_ai_t4_format/bounding_box_2d"]["id"]] == uai_format.BoundingBox2d.fromdict(
        json_data["_understand_ai_t4_format/bounding_box_2d"]
    )
    assert frame.annotations[json_data["_understand_ai_t4_format/polyline_2d"]["id"]] == uai_format.Polyline2d.fromdict(
        json_data["_understand_ai_t4_format/polyline_2d"]
    )
    assert frame.annotations[json_data["_understand_ai_t4_format/polygon_2d"]["id"]] == uai_format.Polygon2d.fromdict(
        json_data["_understand_ai_t4_format/polygon_2d"]
    )
    assert frame.annotations[json_data["_understand_ai_t4_format/bounding_box_3d"]["id"]] == uai_format.BoundingBox3d.fromdict(
        json_data["_understand_ai_t4_format/bounding_box_3d"]
    )
    assert frame.annotations[json_data["_understand_ai_t4_format/segmentation_3d"]["id"]] == uai_format.Segmentation3d.fromdict(
        json_data["_understand_ai_t4_format/segmentation_3d"]
    )

# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
