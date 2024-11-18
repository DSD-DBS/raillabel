# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Point3d

# == Fixtures =========================


@pytest.fixture
def point3d_json() -> dict:
    return [419, 3.14, 0]


@pytest.fixture
def point3d() -> dict:
    return Point3d(419, 3.14, 0)


@pytest.fixture
def another_point3d_json() -> dict:
    return [419.2, 3.34, 0.2]


@pytest.fixture
def another_point3d() -> dict:
    return Point3d(419.2, 3.34, 0.2)


# == Tests ============================


def test_from_json(point3d, point3d_json):
    actual = Point3d.from_json(point3d_json)
    assert actual == point3d


def test_from_json__another(another_point3d, another_point3d_json):
    actual = Point3d.from_json(another_point3d_json)
    assert actual == another_point3d


def test_to_json(point3d, point3d_json):
    actual = point3d.to_json()
    assert actual == tuple(point3d_json)


def test_to_json__another(another_point3d, another_point3d_json):
    actual = another_point3d.to_json()
    assert actual == tuple(another_point3d_json)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
