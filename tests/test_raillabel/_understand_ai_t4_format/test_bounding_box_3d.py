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
    input_data = json_data["_understand_ai_t4_format/bounding_box_3d"]
    input_data["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_lidar"]
    bounding_box = uai_format.BoundingBox3d.fromdict(input_data)

    assert bounding_box.id == UUID(input_data["id"])
    assert bounding_box.object_id == UUID(input_data["objectId"])
    assert bounding_box.class_name == input_data["className"]
    assert bounding_box.size == uai_format.Size3d.fromdict(input_data["geometry"]["size"])
    assert bounding_box.center == uai_format.Point3d.fromdict(input_data["geometry"]["center"])
    assert bounding_box.quaternion == uai_format.Quaternion.fromdict(input_data["geometry"]["quaternion"])
    assert bounding_box.attributes == input_data["attributes"]
    assert bounding_box.sensor == uai_format.SensorReference.fromdict(input_data["sensor"])


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
