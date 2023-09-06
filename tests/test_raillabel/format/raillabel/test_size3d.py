# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Size3d

# == Fixtures =========================

@pytest.fixture
def size3d_dict() -> dict:
    return [0.35, 0.7, 1.92]

@pytest.fixture
def size3d() -> dict:
    return Size3d(0.35, 0.7, 1.92)

# == Tests ============================

def test_fromdict():
    size3d = Size3d.fromdict(
        [0.35, 0.7, 1.92]
    )

    assert size3d.x == 0.35
    assert size3d.y == 0.7
    assert size3d.z == 1.92


def test_asdict():
    size3d = Size3d(
        x=0.35,
        y=0.7,
        z=1.92
    )

    assert size3d.asdict() == [0.35, 0.7, 1.92]


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
