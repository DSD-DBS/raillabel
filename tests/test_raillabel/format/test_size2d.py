# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Size2d

# == Fixtures =========================


@pytest.fixture
def size2d_json() -> dict:
    return [25, 1.344]


@pytest.fixture
def size2d() -> dict:
    return Size2d(25, 1.344)


# == Tests ============================


def test_from_json(size2d, size2d_json):
    actual = Size2d.from_json(size2d_json)
    assert actual == size2d


def test_to_json(size2d, size2d_json):
    actual = size2d.to_json()
    assert actual == tuple(size2d_json)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
