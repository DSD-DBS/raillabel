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
        "id": "0f90cffa-2b6b-4e09-8fc2-527769a94e0a",
        "objectId": "58e7edd8-a7ee-4775-a837-e6dd375e8150",
        "className": "2D_signal_pole",
        "geometry": {
            "points": [
                [
                    127.71153737657284,
                    -0.3861000079676791
                ],
                [
                    127.4762636010818,
                    328.04436391207815
                ],
                [
                    115.77703250958459,
                    334.4789410124016
                ],
                [
                    115.01063176442402,
                    411.0810690770479
                ]
            ]
        },
        "attributes": {
            "structure": "structured",
            "isTruncatedTop": True,
            "isTruncatedBottom": False,
            "occlusion": "0-25%"
        },
        "sensor": {
            "type": "ir_left",
            "uri": "A0001780_image/000_1632321843.100464380.png",
            "timestamp": "1632321843.100464380"
        }
    }
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
