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
    input_data = json_data["_understand_ai_t4_format/polyline_2d"]
    input_data["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_camera"]
    polyline = uai_format.Polyline2d.fromdict(input_data)

    assert polyline.id == UUID(input_data["id"])
    assert polyline.object_id == UUID(input_data["objectId"])
    assert polyline.class_name == input_data["className"]
    assert polyline.points == [(p[0], p[1]) for p in input_data["geometry"]["points"]]
    assert polyline.attributes == input_data["attributes"]
    assert polyline.sensor == uai_format.SensorReference.fromdict(input_data["sensor"])

def test_to_raillabel(json_data):
    input_data = json_data["_understand_ai_t4_format/polyline_2d"]
    input_data["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_camera"]
    polyline = uai_format.Polyline2d.fromdict(input_data)
    output_data, object_id, class_name, sensor_ref = polyline.to_raillabel()
    ground_truth = json_data["_understand_ai_t4_format/polyline_2d_raillabel"]

    assert output_data["name"] == ground_truth["name"]
    assert output_data["val"] == ground_truth["val"]
    assert output_data["attributes"] == ground_truth["attributes"]
    assert output_data["closed"] == False
    assert output_data["mode"] == "MODE_POLY2D_ABSOLUTE"
    assert object_id == input_data["objectId"]
    assert class_name == "track"
    assert sensor_ref == polyline.sensor.to_raillabel()[1]


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
