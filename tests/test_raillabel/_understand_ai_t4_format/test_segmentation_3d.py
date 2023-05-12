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
    input_data = json_data["_understand_ai_t4_format/segmentation_3d"]
    input_data["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_lidar"]
    segmentation_3d = uai_format.Segmentation3d.fromdict(input_data)

    assert segmentation_3d.id == UUID(input_data["id"])
    assert segmentation_3d.object_id == UUID(input_data["objectId"])
    assert segmentation_3d.class_name == input_data["className"]
    assert segmentation_3d.associated_points == input_data["geometry"]["associatedPoints"]
    assert segmentation_3d.number_of_points == input_data["geometry"]["numberOfPointsInBox"]
    assert segmentation_3d.attributes == input_data["attributes"]
    assert segmentation_3d.sensor == uai_format.SensorReference.fromdict(input_data["sensor"])


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
