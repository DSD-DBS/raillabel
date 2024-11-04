# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Size2d

# == Fixtures =========================


@pytest.fixture
def size2d_dict() -> dict:
    return [25, 1.344]


@pytest.fixture
def size2d() -> dict:
    return Size2d(25, 1.344)


# == Tests ============================


def test_from_json(size2d, size2d_dict):
    actual = Size2d.from_json(size2d_dict)
    assert actual == size2d


def test_fromdict():
    size2d = Size2d.fromdict([25, 1.344])

    assert size2d.x == 25
    assert size2d.y == 1.344


def test_asdict():
    size2d = Size2d(
        x=25,
        y=1.344,
    )

    assert size2d.asdict() == [25, 1.344]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
