# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

import pytest

from raillabel.json_format import JSONObject, JSONFrameInterval, JSONElementDataPointer
from raillabel.format import Object

# == Fixtures =========================


@pytest.fixture
def objects(object_person, object_person_id, object_track, object_track_id) -> dict[UUID, Object]:
    return {
        object_person_id: object_person,
        object_track_id: object_track,
    }


@pytest.fixture
def object_person_json() -> JSONObject:
    return JSONObject(
        name="person_0032",
        type="person",
        frame_intervals=[JSONFrameInterval(frame_start=1, frame_end=1)],
        object_data_pointers={
            "rgb_center__bbox__person": JSONElementDataPointer(
                frame_intervals=[JSONFrameInterval(frame_start=1, frame_end=1)],
                type="bbox",
                attribute_pointers={
                    "has_red_hat": "boolean",
                    "has_green_hat": "boolean",
                    "number_of_red_clothing_items": "num",
                    "color_of_hat": "text",
                    "clothing_items": "vec",
                },
            ),
            "lidar__cuboid__person": JSONElementDataPointer(
                frame_intervals=[JSONFrameInterval(frame_start=1, frame_end=1)],
                type="cuboid",
                attribute_pointers={
                    "has_red_hat": "boolean",
                    "has_green_hat": "boolean",
                    "number_of_red_clothing_items": "num",
                    "color_of_hat": "text",
                    "clothing_items": "vec",
                },
            ),
            "lidar__vec__person": JSONElementDataPointer(
                frame_intervals=[JSONFrameInterval(frame_start=1, frame_end=1)],
                type="vec",
                attribute_pointers={
                    "has_red_hat": "boolean",
                    "has_green_hat": "boolean",
                    "number_of_red_clothing_items": "num",
                    "color_of_hat": "text",
                    "clothing_items": "vec",
                },
            ),
        },
    )


@pytest.fixture
def object_person() -> Object:
    return Object(
        name="person_0032",
        type="person",
    )


@pytest.fixture
def object_person_id() -> UUID:
    return UUID("b40ba3ad-0327-46ff-9c28-2506cfd6d934")


@pytest.fixture
def object_track_json() -> JSONObject:
    return JSONObject(
        name="track_0001",
        type="track",
        frame_intervals=[JSONFrameInterval(frame_start=1, frame_end=1)],
        object_data_pointers={
            "rgb_center__poly2d__track": JSONElementDataPointer(
                frame_intervals=[JSONFrameInterval(frame_start=1, frame_end=1)],
                type="poly2d",
                attribute_pointers={
                    "has_red_hat": "boolean",
                    "has_green_hat": "boolean",
                    "number_of_red_clothing_items": "num",
                    "color_of_hat": "text",
                    "clothing_items": "vec",
                },
            ),
            "lidar__poly3d__track": JSONElementDataPointer(
                frame_intervals=[JSONFrameInterval(frame_start=1, frame_end=1)],
                type="poly3d",
                attribute_pointers={
                    "has_red_hat": "boolean",
                    "has_green_hat": "boolean",
                    "number_of_red_clothing_items": "num",
                    "color_of_hat": "text",
                    "clothing_items": "vec",
                },
            ),
        },
    )


@pytest.fixture
def object_track() -> Object:
    return Object(
        name="track_0001",
        type="track",
    )


@pytest.fixture
def object_track_id() -> UUID:
    return UUID("cfcf9750-3BC3-4077-9079-a82c0c63976a")


# == Tests ============================


def test_from_json__person(object_person, object_person_json):
    actual = Object.from_json(object_person_json)
    assert actual == object_person


def test_from_json__track(object_track, object_track_json):
    actual = Object.from_json(object_track_json)
    assert actual == object_track


def test_to_json__person(object_person, object_person_json, object_person_id, frame):
    actual = object_person.to_json(object_person_id, {1: frame})
    assert actual == object_person_json


def test_to_json__track(object_track, object_track_json, object_track_id, frame):
    actual = object_track.to_json(object_track_id, {1: frame})
    assert actual == object_track_json


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
