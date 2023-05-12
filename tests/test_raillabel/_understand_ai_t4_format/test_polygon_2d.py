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
    input_data = json_data["_understand_ai_t4_format/polygon_2d"]
    input_data["sensor"] = json_data["_understand_ai_t4_format/sensor_reference_camera"]
    polygon = uai_format.Polygon2d.fromdict(input_data)

    assert polygon.id == UUID(input_data["id"])
    assert polygon.object_id == UUID(input_data["objectId"])
    assert polygon.class_name == input_data["className"]
    assert polygon.points == [(p[0], p[1]) for p in input_data["geometry"]["points"]]
    assert polygon.attributes == input_data["attributes"]
    assert polygon.sensor == uai_format.SensorReference.fromdict(input_data["sensor"])


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
