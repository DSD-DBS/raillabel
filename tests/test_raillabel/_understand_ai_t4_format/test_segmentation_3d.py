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
        "id": "13478f94-d556-4f64-a72b-47662e94988e",
        "objectId": "05a7e7a7-91e1-49ef-a172-780f2461f013",
        "className": "3D_catenary_pole",
        "geometry": {
            "associatedPoints": [
                39814,
                39815,
                39816,
                39817,
                39818
            ],
            "numberOfPointsInBox": 5
        },
        "attributes": {
            "structure": "structured"
        },
        "sensor": {
            "type": "LIDAR",
            "uri": "lidar_merged/000_1632321880.132833000.pcd",
            "timestamp": "1632321880.132833000"
        }
    }
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
