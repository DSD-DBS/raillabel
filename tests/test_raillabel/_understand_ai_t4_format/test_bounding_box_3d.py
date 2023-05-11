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
            "size": {
                "height": 12.887274595406309,
                "width": 0.9726718154765793,
                "length": 0.7487449536720978
            },
            "center": {
                "x": 27.075067129430366,
                "y": -3.7850908693727328,
                "z": 6.671744016124283
            },
            "quaternion": {
                "x": -7.710484478135359e-17,
                "y": -7.978951661384013e-17,
                "z": 0.7191010536652217,
                "w": 0.6949055148849863
            }
        },
        "attributes": {
            "isDummy": False,
            "carries": "nothing",
            "connectedTo": [],
            "pose": "upright",
        },
        "sensor": {
            "type": "LIDAR",
            "uri": "lidar_merged/000_1632321880.132833000.pcd",
            "timestamp": "1632321880.132833000"
        }
    }
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
