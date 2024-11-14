# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

import pytest

from raillabel.format import Num
from raillabel.json_format import JSONNum

# == Fixtures =========================


@pytest.fixture
def num_json(num_id) -> JSONNum:
    return JSONNum(
        uid=num_id,
        name="velocity",
        val=49.21321,
        coordinate_system="gps_imu",
    )


@pytest.fixture
def num_id() -> UUID:
    return UUID("78f0ad89-2750-4a30-9d66-44c9da73a714")


@pytest.fixture
def num(num_id) -> Num:
    return Num(
        sensor_id="gps_imu",
        name="velocity",
        val=49.21321,
        id=num_id,
    )


# == Tests ============================


def test_from_json(num, num_json):
    actual = Num.from_json(num_json)
    assert actual == num


def test_to_json(num, num_json):
    actual = num.to_json()
    assert actual == num_json


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
