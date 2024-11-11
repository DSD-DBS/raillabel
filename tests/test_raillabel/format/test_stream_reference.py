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


# == Tests ============================


def test_from_json(sensor_reference, sensor_reference_json):
    actual = SensorReference.from_json(sensor_reference_json)
    assert actual == sensor_reference


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
