# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel._understand_ai_t4_format as uai_format


def test_fromdict():
    input_data = {
        "x": -7.710484478135359e-17,
        "y": -7.978951661384013e-17,
        "z": 0.7191010536652217,
        "w": 0.6949055148849863
    }
    quaternion = uai_format.Quaternion.fromdict(input_data)

    assert quaternion.x == float(input_data["x"])
    assert quaternion.y == float(input_data["y"])
    assert quaternion.z == float(input_data["z"])
    assert quaternion.w == float(input_data["w"])

# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
