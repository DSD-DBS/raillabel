# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Point2d

# == Fixtures =========================


@pytest.fixture
def point2d_json() -> dict:
    return [1.5, 222]


@pytest.fixture
def point2d() -> dict:
    return Point2d(1.5, 222)


# == Tests ============================


def test_from_json(point2d, point2d_json):
    actual = Point2d.from_json(point2d_json)
    assert actual == point2d


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
