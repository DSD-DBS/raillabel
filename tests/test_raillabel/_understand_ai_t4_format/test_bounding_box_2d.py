# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path
from uuid import UUID

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel._understand_ai_t4_format as uai_format


def test_fromdict():
    input_data = {
        "id": "2f2a1d7f-56d1-435c-a3ec-d6b8fdaaa965",
        "objectId": "48c988bd-76f1-423f-b46d-7e7acb859f31",
        "className": "test_class",
        "geometry": {
            "xMin": 1,
            "yMin": 2,
            "xMax": 3,
            "yMax": 4
        },
        "attributes": {
            "isDummy": False,
            "carries": "nothing",
            "connectedTo": [],
            "pose": "upright",
        },
        "sensor": {
            "type": "ir_middle",
            "uri": "A0001781_image/000_1632321843.100464760.png",
            "timestamp": "1632321843.100464760"
        }
    }
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


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
