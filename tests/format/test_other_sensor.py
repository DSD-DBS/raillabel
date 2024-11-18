# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import OtherSensor
from raillabel.json_format import JSONCoordinateSystem, JSONStreamOther

# == Fixtures =========================


@pytest.fixture
def other_json(transform_json) -> tuple[JSONStreamOther, JSONCoordinateSystem]:
    return (
        JSONStreamOther(
            type="other",
            uri="/path/to/sensor/data",
            description="A very nice generic sensor",
        ),
        JSONCoordinateSystem(
            parent="base", type="sensor", pose_wrt_parent=transform_json, children=None
        ),
    )


@pytest.fixture
def other(transform) -> dict:
    return OtherSensor(
        extrinsics=transform,
        uri="/path/to/sensor/data",
        description="A very nice generic sensor",
    )


# == Tests ============================


def test_from_json(other, other_json):
    actual = OtherSensor.from_json(other_json[0], other_json[1])
    assert actual == other


def test_to_json(other, other_json):
    actual = other.to_json()
    assert actual == other_json


if __name__ == "__main__":
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
