# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

import pytest

from raillabel.json_format import JSONObject
from raillabel.format import Object

# == Fixtures =========================


@pytest.fixture
def object_person_json() -> JSONObject:
    return JSONObject(
        name="person_0032",
        type="person",
    )


@pytest.fixture
def object_person() -> Object:
    return Object(
        name="person_0032",
        type="person",
    )


@pytest.fixture
def object_person_uid() -> UUID:
    return UUID("b40ba3ad-0327-46ff-9c28-2506cfd6d934")


@pytest.fixture
def object_track_json() -> JSONObject:
    return JSONObject(
        name="track_0001",
        type="track",
    )


@pytest.fixture
def object_track() -> Object:
    return Object(
        name="track_0001",
        type="track",
    )


@pytest.fixture
def object_track_uid() -> UUID:
    return UUID("cfcf9750-3BC3-4077-9079-a82c0c63976a")


# == Tests ============================


def test_from_json__person(object_person, object_person_json):
    actual = Object.from_json(object_person_json)
    assert actual == object_person


def test_from_json__track(object_track, object_track_json):
    actual = Object.from_json(object_track_json)
    assert actual == object_track


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
