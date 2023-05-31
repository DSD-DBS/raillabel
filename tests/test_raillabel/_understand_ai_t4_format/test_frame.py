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


def _prepare_ground_truth(ground_truth: dict, json_data:dict) -> dict:
    ground_truth["objects"]["48c988bd-76f1-423f-b46d-7e7acb859f31"]["object_data"]["bbox"] = [
        json_data["_understand_ai_t4_format/bounding_box_2d_raillabel"]
    ]
    ground_truth["objects"]["48c988bd-76f1-423f-b46d-7e7acb859f31"]["object_data"]["cuboid"] = [
        json_data["_understand_ai_t4_format/bounding_box_3d_raillabel"]
    ]
    ground_truth["objects"]["58e7edd8-a7ee-4775-a837-e6dd375e8150"]["object_data"]["poly2d"] = [
        json_data["_understand_ai_t4_format/polygon_2d_raillabel"]
    ]
    ground_truth["objects"]["4d8eca35-6c1d-4159-8062-21c2f2c051df"]["object_data"]["poly2d"] = [
        json_data["_understand_ai_t4_format/polyline_2d_raillabel"]
    ]
    ground_truth["objects"]["05a7e7a7-91e1-49ef-a172-780f2461f013"]["object_data"]["vec"] = [
        json_data["_understand_ai_t4_format/segmentation_3d_raillabel"]
    ]

    return ground_truth


def test_fromdict(json_data):
    input_data = _prepare_frame_data(json_data["_understand_ai_t4_format/frame"], json_data)
    frame = uai_format.Frame.fromdict(input_data)

    assert frame.id == int(input_data["frameId"])
    assert frame.timestamp == Decimal(input_data["timestamp"])
    assert frame.bounding_box_2ds[json_data["_understand_ai_t4_format/bounding_box_2d"]["id"]] == uai_format.BoundingBox2d.fromdict(
        json_data["_understand_ai_t4_format/bounding_box_2d"]
    )
    assert frame.polyline_2ds[json_data["_understand_ai_t4_format/polyline_2d"]["id"]] == uai_format.Polyline2d.fromdict(
        json_data["_understand_ai_t4_format/polyline_2d"]
    )
    assert frame.polygon_2ds[json_data["_understand_ai_t4_format/polygon_2d"]["id"]] == uai_format.Polygon2d.fromdict(
        json_data["_understand_ai_t4_format/polygon_2d"]
    )
    assert frame.bounding_box_3ds[json_data["_understand_ai_t4_format/bounding_box_3d"]["id"]] == uai_format.BoundingBox3d.fromdict(
        json_data["_understand_ai_t4_format/bounding_box_3d"]
    )
    assert frame.segmentation_3ds[json_data["_understand_ai_t4_format/segmentation_3d"]["id"]] == uai_format.Segmentation3d.fromdict(
        json_data["_understand_ai_t4_format/segmentation_3d"]
    )

def test_to_raillabel(json_data):
    input_data = _prepare_frame_data(json_data["_understand_ai_t4_format/frame"], json_data)
    frame = uai_format.Frame.fromdict(input_data)
    output_data = frame.to_raillabel()
    ground_truth = _prepare_ground_truth(json_data["_understand_ai_t4_format/frame_raillabel"], json_data)

    assert output_data == ground_truth

def test_translated_sensors(json_data):
    input_data = _prepare_frame_data(json_data["_understand_ai_t4_format/frame"], json_data)
    frame = uai_format.Frame.fromdict(input_data)
    ground_truth_streams = json_data["_understand_ai_t4_format/frame_raillabel"]["frame_properties"]["streams"]

    assert frame.translated_sensors.keys() == ground_truth_streams.keys()

def test_translated_objects(json_data):
    input_data = _prepare_frame_data(json_data["_understand_ai_t4_format/frame"], json_data)
    frame = uai_format.Frame.fromdict(input_data)
    ground_truth_objects = json_data["_understand_ai_t4_format/frame_raillabel"]["objects"]

    assert frame.translated_objects.keys() == ground_truth_objects.keys()


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
