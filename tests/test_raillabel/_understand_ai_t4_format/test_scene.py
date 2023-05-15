# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from test_frame import _prepare_frame_data

import raillabel._understand_ai_t4_format as uai_format


def test_fromdict(json_data):
    input_data = {
        "metadata": json_data["_understand_ai_t4_format/metadata"],
        "coordinateSystems": [
            json_data["_understand_ai_t4_format/coordinate_system_camera"],
            json_data["_understand_ai_t4_format/coordinate_system_lidar"],
        ],
        "frames": [
            _prepare_frame_data(json_data["_understand_ai_t4_format/frame"], json_data),
        ]
    }
    scene = uai_format.Scene.fromdict(input_data)

    assert scene.metadata == uai_format.Metadata.fromdict(input_data["metadata"])
    assert len(scene.coordinate_systems) == 2
    assert scene.coordinate_systems[input_data["coordinateSystems"][0]["coordinate_system_id"]] == uai_format.CoordinateSystem.fromdict(input_data["coordinateSystems"][0])
    assert scene.coordinate_systems[input_data["coordinateSystems"][1]["coordinate_system_id"]] == uai_format.CoordinateSystem.fromdict(input_data["coordinateSystems"][1])
    assert len(scene.frames) == 1
    assert scene.frames[input_data["frames"][0]["frameId"]] == uai_format.Frame.fromdict(input_data["frames"][0])


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
