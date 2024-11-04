# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Point3d

# == Fixtures =========================


@pytest.fixture
def point3d_dict() -> dict:
    return [419, 3.14, 0]


@pytest.fixture
def point3d() -> dict:
    return Point3d(419, 3.14, 0)


@pytest.fixture
def point3d_another_dict() -> dict:
    return [9, 8, 7]


@pytest.fixture
def point3d_another() -> dict:
    return Point3d(9, 8, 7)


# == Tests ============================


def test_from_json(point3d, point3d_dict):
    actual = Point3d.from_json(point3d_dict)
    assert actual == point3d


def test_fromdict():
    point3d = Point3d.fromdict([419, 3.14, 0])

    assert point3d.x == 419
    assert point3d.y == 3.14
    assert point3d.z == 0


def test_asdict():
    point3d = Point3d(
        x=419,
        y=3.14,
        z=0,
    )

    assert point3d.asdict() == [419, 3.14, 0]


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
