# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Quaternion

# == Fixtures =========================


@pytest.fixture
def quaternion_json() -> dict:
    return [0.75318325, -0.10270147, 0.21430262, -0.61338551]


@pytest.fixture
def quaternion() -> dict:
    return Quaternion(0.75318325, -0.10270147, 0.21430262, -0.61338551)


# == Tests ============================


def test_from_json(quaternion, quaternion_json):
    actual = Quaternion.from_json(quaternion_json)
    assert actual == quaternion


def test_to_json(quaternion, quaternion_json):
    actual = quaternion.to_json()
    assert actual == tuple(quaternion_json)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
