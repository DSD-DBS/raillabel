# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest
from decimal import Decimal

from raillabel.format import SensorReference
from raillabel.json_format import JSONStreamSync, JSONStreamSyncProperties, JSONStreamSyncTimestamp

# == Fixtures =========================


@pytest.fixture
def sensor_reference_json() -> JSONStreamSync:
    return JSONStreamSync(
        stream_properties=JSONStreamSyncProperties(
            sync=JSONStreamSyncTimestamp(timestamp="1631337747.123123123")
        ),
        uri="/uri/to/file.png",
    )


@pytest.fixture
def sensor_reference() -> SensorReference:
    return SensorReference(timestamp=Decimal("1631337747.123123123"), uri="/uri/to/file.png")


@pytest.fixture
def another_sensor_reference_json() -> JSONStreamSync:
    return JSONStreamSync(
        stream_properties=JSONStreamSyncProperties(
            sync=JSONStreamSyncTimestamp(timestamp="1631337747.103123123")
        ),
        uri="/uri/to/file.pcd",
    )


@pytest.fixture
def another_sensor_reference() -> SensorReference:
    return SensorReference(timestamp=Decimal("1631337747.103123123"), uri="/uri/to/file.pcd")


# == Tests ============================


def test_from_json(sensor_reference, sensor_reference_json):
    actual = SensorReference.from_json(sensor_reference_json)
    assert actual == sensor_reference


def test_from_json__another(another_sensor_reference, another_sensor_reference_json):
    actual = SensorReference.from_json(another_sensor_reference_json)
    assert actual == another_sensor_reference


def test_to_json(sensor_reference, sensor_reference_json):
    actual = sensor_reference.to_json()
    assert actual == sensor_reference_json


def test_to_json__another(another_sensor_reference, another_sensor_reference_json):
    actual = another_sensor_reference.to_json()
    assert actual == another_sensor_reference_json


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
