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
        uid="78f0ad89-2750-4a30-9d66-44c9da73a714",
        name="rgb_middle__bbox__person",
        val=point2d_json + size2d_json,
        coordinate_system="rgb_middle",
        attributes=attributes_multiple_types_json,
    )


@pytest.fixture
def bbox(
    point2d,
    size2d,
    attributes_multiple_types,
) -> dict:
    return Bbox(
        pos=point2d,
        size=size2d,
        sensor="rgb_middle",
        attributes=attributes_multiple_types,
        object=UUID("b40ba3ad-0327-46ff-9c28-2506cfd6d934"),
    )


# == Tests ============================


def test_from_json(bbox, bbox_json):
    actual = Bbox.from_json(bbox_json, object_uid="b40ba3ad-0327-46ff-9c28-2506cfd6d934")
    assert actual == bbox


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
