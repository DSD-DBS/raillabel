# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

import raillabel.format.understand_ai as uai_format

# == Fixtures =========================

@pytest.fixture
def point_3d_uai_dict() -> dict:
    return {
        "x": 0,
        "y": 1,
        "z": 2,
    }

@pytest.fixture
def point_3d_uai() -> dict:
    return uai_format.Point3d(
        x=0,
        y=1,
        z=2,
    )

@pytest.fixture
def point_3d_vec() -> dict:
    return [0, 1, 2]

# == Tests ============================

def test_fromdict():
    point_3d = uai_format.Point3d.fromdict(
        {
            "x": 0,
            "y": 1,
            "z": 2,
        }
    )

    assert point_3d.x == 0
    assert point_3d.y == 1
    assert point_3d.z == 2


if __name__ == "__main__":
    import os
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
