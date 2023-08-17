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
        "x": 27.075067129430366,
        "y": -3.7850908693727328,
        "z": 6.671744016124283
    }
    point = uai_format.Point3d.fromdict(input_data)

    assert point.x == float(input_data["x"])
    assert point.y == float(input_data["y"])
    assert point.z == float(input_data["z"])

# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
