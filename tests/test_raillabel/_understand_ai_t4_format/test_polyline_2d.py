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
        "id": "7f2b99b7-61e4-4f9f-96e9-d3e9f583d7c2",
        "objectId": "4d8eca35-6c1d-4159-8062-21c2f2c051df",
        "className": "ir_track",
        "geometry": {
            "points": [
                [
                    493.20616179847406,
                    479.9728191806302
                ],
                [
                    542.6546426503735,
                    431.74800354374366
                ],
                [
                    589.9350150621058,
                    385.51547643522207
                ],
                [
                    639.9702598289472,
                    335.8846553104306
                ]
            ]
        },
        "attributes": {
            "trackId": "left_first_track",
            "railSide": "rightRail",
            "occlusion": "0-25%"
        },
        "sensor": {
            "type": "ir_left",
            "uri": "A0001780_image/000_1632321843.100464380.png",
            "timestamp": "1632321843.100464380"
        }
    }
    polyline = uai_format.Polyline2d.fromdict(input_data)

    assert polyline.id == UUID(input_data["id"])
    assert polyline.object_id == UUID(input_data["objectId"])
    assert polyline.class_name == input_data["className"]
    assert polyline.points == [(p[0], p[1]) for p in input_data["geometry"]["points"]]
    assert polyline.attributes == input_data["attributes"]
    assert polyline.sensor == uai_format.SensorReference.fromdict(input_data["sensor"])


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
