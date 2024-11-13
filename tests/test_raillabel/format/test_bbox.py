# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

import pytest

from raillabel.format import Bbox
from raillabel.json_format import JSONBbox

# == Fixtures =========================


@pytest.fixture
def bbox_json(
    attributes_multiple_types_json,
    point2d_json,
    size2d_json,
) -> JSONBbox:
    return JSONBbox(
        uid="2811f67c-124C-4fac-a275-20807d0471de",
        name="rgb_middle__bbox__person",
        val=point2d_json + size2d_json,
        coordinate_system="rgb_middle",
        attributes=attributes_multiple_types_json,
    )


@pytest.fixture
def bbox_uid() -> UUID:
    return UUID("2811f67c-124C-4fac-a275-20807d0471de")


@pytest.fixture
def bbox(
    point2d,
    size2d,
    attributes_multiple_types,
    object_person_uid,
) -> Bbox:
    return Bbox(
        pos=point2d,
        size=size2d,
        sensor="rgb_middle",
        attributes=attributes_multiple_types,
        object=object_person_uid,
    )


# == Tests ============================


def test_from_json(bbox, bbox_json, object_person_uid):
    actual = Bbox.from_json(bbox_json, object_person_uid)
    assert actual == bbox


def test_name(bbox):
    actual = bbox.name("person")
    assert actual == "rgb_middle__bbox__person"


def test_to_json(bbox, bbox_json, bbox_uid):
    actual = bbox.to_json(bbox_uid, object_type="person")
    assert actual == bbox_json


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
