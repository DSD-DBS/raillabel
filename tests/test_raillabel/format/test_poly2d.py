# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

import pytest

from raillabel.format import Poly2d
from raillabel.json_format import JSONPoly2d

# == Fixtures =========================


@pytest.fixture
def poly2d_json(
    point2d_json,
    another_point2d_json,
    attributes_multiple_types_json,
) -> JSONPoly2d:
    return JSONPoly2d(
        uid="013e7b34-62E5-435c-9412-87318c50f6d8",
        name="rgb_middle__poly2d__person",
        closed=True,
        mode="MODE_POLY2D_ABSOLUTE",
        val=point2d_json + another_point2d_json,
        coordinate_system="rgb_middle",
        attributes=attributes_multiple_types_json,
    )


@pytest.fixture
def poly2d_uid() -> UUID:
    return UUID("013e7b34-62E5-435c-9412-87318c50f6d8")


@pytest.fixture
def poly2d(
    point2d,
    another_point2d,
    attributes_multiple_types,
) -> Poly2d:
    return Poly2d(
        points=[point2d, another_point2d],
        closed=True,
        sensor="rgb_middle",
        attributes=attributes_multiple_types,
        object=UUID("cfcf9750-3BC3-4077-9079-a82c0c63976a"),
    )


# == Tests ============================


def test_from_json(poly2d, poly2d_json):
    actual = Poly2d.from_json(poly2d_json, object_uid=UUID("cfcf9750-3BC3-4077-9079-a82c0c63976a"))
    assert actual == poly2d


def test_name(poly2d):
    actual = poly2d.name("person")
    assert actual == "rgb_middle__poly2d__person"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
