# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Point2d

# == Fixtures =========================


@pytest.fixture
def point2d_json() -> tuple[float, float]:
    return [1.5, 222]


@pytest.fixture
def point2d() -> Point2d:
    return Point2d(1.5, 222)


@pytest.fixture
def another_point2d_json() -> tuple[float, float]:
    return [1.7, 222.2]


@pytest.fixture
def another_point2d() -> Point2d:
    return Point2d(1.7, 222.2)


# == Tests ============================


def test_from_json(point2d, point2d_json):
    actual = Point2d.from_json(point2d_json)
    assert actual == point2d


def test_from_json__another(another_point2d, another_point2d_json):
    actual = Point2d.from_json(another_point2d_json)
    assert actual == another_point2d


def test_to_json(point2d, point2d_json):
    actual = point2d.to_json()
    assert actual == tuple(point2d_json)


def test_to_json__another(another_point2d, another_point2d_json):
    actual = another_point2d.to_json()
    assert actual == tuple(another_point2d_json)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
