# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.json_format import (
    JSONAttributes,
    JSONBooleanAttribute,
    JSONNumAttribute,
    JSONTextAttribute,
    JSONVecAttribute,
)
from raillabel.format._attributes import (
    _attributes_from_json,
    _attributes_to_json,
    UnsupportedAttributeTypeError,
)

# == Fixtures =========================


@pytest.fixture
def attributes_multiple_types_json() -> JSONAttributes:
    return JSONAttributes(
        boolean=[
            JSONBooleanAttribute(name="has_red_hat", val=True),
            JSONBooleanAttribute(name="has_green_hat", val=False),
        ],
        num=[JSONNumAttribute(name="number_of_red_clothing_items", val=2)],
        text=[JSONTextAttribute(name="color_of_hat", val="red")],
        vec=[
            JSONVecAttribute(
                name="clothing_items", val=["red_hat", "brown_coat", "black_pants", "red_shoes"]
            )
        ],
    )


@pytest.fixture
def attributes_multiple_types() -> dict:
    return {
        "has_red_hat": True,
        "has_green_hat": False,
        "number_of_red_clothing_items": 2,
        "color_of_hat": "red",
        "clothing_items": ["red_hat", "brown_coat", "black_pants", "red_shoes"],
    }


# == Tests ============================


def test_attributes_from_json__none():
    actual = _attributes_from_json(None)
    assert actual == {}


def test_attributes_from_json__empty():
    json_attributes = JSONAttributes(
        boolean=None,
        num=None,
        text=None,
        vec=None,
    )

    actual = _attributes_from_json(json_attributes)
    assert actual == {}


def test_attributes_from_json__multiple_types(
    attributes_multiple_types, attributes_multiple_types_json
):
    actual = _attributes_from_json(attributes_multiple_types_json)
    assert actual == attributes_multiple_types


def test_attributes_to_json__empty():
    actual = _attributes_to_json({})
    assert actual == None


def test_attributes_to_json__multiple_types(
    attributes_multiple_types, attributes_multiple_types_json
):
    actual = _attributes_to_json(attributes_multiple_types)
    assert actual == attributes_multiple_types_json


def test_attributes_to_json__unsupported_type():
    with pytest.raises(UnsupportedAttributeTypeError):
        _attributes_to_json({"attribute_with_unsupported_type": object})


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
