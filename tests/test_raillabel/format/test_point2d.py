# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

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


def test_from_json(point2d, point2d_dict):
    actual = Point2d.from_json(point2d_dict)
    assert actual == point2d


def test_fromdict():
    point2d = Point2d.fromdict([1.5, 222])

    assert point2d.x == 1.5
    assert point2d.y == 222


def test_asdict():
    point2d = Point2d(
        x=1.5,
        y=222,
    )

    assert point2d.asdict() == [1.5, 222]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
