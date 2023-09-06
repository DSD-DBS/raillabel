# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Quaternion

# == Fixtures =========================

@pytest.fixture
def quaternion_dict() -> dict:
    return [0.75318325, -0.10270147,  0.21430262, -0.61338551]

@pytest.fixture
def quaternion() -> dict:
    return Quaternion(0.75318325, -0.10270147,  0.21430262, -0.61338551)

# == Tests ============================

def test_fromdict():
    quaternion = Quaternion.fromdict(
        [
            0.75318325,
            -0.10270147,
            0.21430262,
            -0.61338551
        ]
    )

    assert quaternion.x == 0.75318325
    assert quaternion.y == -0.10270147
    assert quaternion.z == 0.21430262
    assert quaternion.w == -0.61338551


def test_asdict():
    quaternion = Quaternion(
        x=0.75318325,
        y=-0.10270147,
        z=0.21430262,
        w=-0.61338551
    )

    assert quaternion.asdict() == [
        0.75318325,
        -0.10270147,
        0.21430262,
        -0.61338551
    ]


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
