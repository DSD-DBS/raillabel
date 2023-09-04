# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Point2d

# == Fixtures =========================

@pytest.fixture
def point2d_dict() -> dict:
    return [1.5, 222]

@pytest.fixture
def point2d() -> dict:
    return Point2d(1.5, 222)


@pytest.fixture
def point2d_another_dict() -> dict:
    return [19, 84]

@pytest.fixture
def point2d_another() -> dict:
    return Point2d(19, 84)

# == Tests ============================

def test_fromdict():
    point2d = Point2d.fromdict(
        [1.5, 222]
    )

    assert point2d.x == 1.5
    assert point2d.y == 222


def test_asdict():
    point2d = Point2d(
        x=1.5,
        y=222,
    )

    assert point2d.asdict() == [1.5, 222]


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
