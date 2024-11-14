# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Size3d

# == Fixtures =========================


@pytest.fixture
def size3d_json() -> dict:
    return [25, 1.344, 12.3]


@pytest.fixture
def size3d() -> dict:
    return Size3d(25, 1.344, 12.3)


# == Tests ============================


def test_from_json(size3d, size3d_json):
    actual = Size3d.from_json(size3d_json)
    assert actual == size3d


def test_to_json(size3d, size3d_json):
    actual = size3d.to_json()
    assert actual == tuple(size3d_json)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
