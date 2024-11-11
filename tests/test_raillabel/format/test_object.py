# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.json_format import JSONObject
from raillabel.format import Object

# == Fixtures =========================


@pytest.fixture
def object_person_json() -> JSONObject:
    return JSONObject(
        name="person0032",
        type="person",
    )


@pytest.fixture
def object_person() -> Object:
    return Object(
        name="person0032",
        type="person",
    )


# == Tests ============================


def test_from_json(object_person, object_person_json):
    actual = Object.from_json(object_person_json)
    assert actual == object_person


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
