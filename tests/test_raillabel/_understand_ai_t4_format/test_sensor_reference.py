# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel._understand_ai_t4_format as uai_format


def test_fromdict(json_data):
    input_data = json_data["_understand_ai_t4_format/sensor_reference_camera"]
    sensor_reference = uai_format.SensorReference.fromdict(input_data)

    assert sensor_reference.type == input_data["type"]
    assert sensor_reference.uri == input_data["uri"]
    assert sensor_reference.timestamp == Decimal(input_data["timestamp"])

def test_to_raillabel(json_data):
    sensor_reference = uai_format.SensorReference.fromdict(
        json_data["_understand_ai_t4_format/sensor_reference_camera"]
    )
    sensor_id, output_data = sensor_reference.to_raillabel()

    assert sensor_id == sensor_reference.type
    assert output_data == {
        "stream_properties": {
            "sync": {
                "timestamp": str(sensor_reference.timestamp)
            }
        },
        "uri": sensor_reference.uri
    }


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
