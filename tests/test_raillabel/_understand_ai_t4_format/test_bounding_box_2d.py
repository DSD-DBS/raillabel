# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path
from uuid import UUID

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel._understand_ai_t4_format as uai_format


def test_fromdict(json_data):
    input_data = json_data["_understand_ai_t4_format/bounding_box_2d"]
    input_data["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_camera"]
    bounding_box = uai_format.BoundingBox2d.fromdict(input_data)

    assert bounding_box.id == UUID(input_data["id"])
    assert bounding_box.object_id == UUID(input_data["objectId"])
    assert bounding_box.class_name == input_data["className"]
    assert bounding_box.x_min == input_data["geometry"]["xMin"]
    assert bounding_box.y_min == input_data["geometry"]["yMin"]
    assert bounding_box.x_max == input_data["geometry"]["xMax"]
    assert bounding_box.y_max == input_data["geometry"]["yMax"]
    assert bounding_box.attributes == input_data["attributes"]
    assert bounding_box.sensor == uai_format.SensorReference.fromdict(input_data["sensor"])

def test_to_raillabel(json_data):
    input_data = json_data["_understand_ai_t4_format/bounding_box_2d"]
    input_data["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_camera"]
    bounding_box = uai_format.BoundingBox2d.fromdict(input_data)
    output_data, object_id, class_name, sensor_ref = bounding_box.to_raillabel()
    ground_truth = json_data["_understand_ai_t4_format/bounding_box_2d_raillabel"]

    assert output_data["name"] == ground_truth["name"]
    assert output_data["val"] == ground_truth["val"]
    assert output_data["attributes"] == ground_truth["attributes"]
    assert object_id == input_data["objectId"]
    assert class_name == input_data["className"]
    assert sensor_ref == bounding_box.sensor.to_raillabel()[1]

# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
