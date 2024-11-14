# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from raillabel.json_format import (
    JSONAttributes,
    JSONBooleanAttribute,
    JSONNumAttribute,
    JSONTextAttribute,
    JSONVecAttribute,
)


def _attributes_from_json(json: JSONAttributes | None) -> dict[str, float | bool | str | list]:
    """Parse the annotation attributes from json."""
    if json is None:
        return {}

    attributes: dict[str, float | bool | str | list] = {}

    if json.boolean is not None:
        for bool_attribute in json.boolean:
            attributes[bool_attribute.name] = bool_attribute.val

    if json.num is not None:
        for num_attribute in json.num:
            attributes[num_attribute.name] = num_attribute.val

    if json.text is not None:
        for text_attribute in json.text:
            attributes[text_attribute.name] = text_attribute.val

    if json.vec is not None:
        for vec_attribute in json.vec:
            attributes[vec_attribute.name] = vec_attribute.val

    return attributes


def _attributes_to_json(attributes: dict[str, float | bool | str | list]) -> JSONAttributes | None:
    if len(attributes) == 0:
        return None

    boolean_attributes = []
    num_attributes = []
    text_attributes = []
    vec_attributes = []

    for name, value in attributes.items():
        if isinstance(value, bool):
            boolean_attributes.append(JSONBooleanAttribute(name=name, val=value))

        elif isinstance(value, (int, float)):
            num_attributes.append(JSONNumAttribute(name=name, val=value))

        elif isinstance(value, str):
            text_attributes.append(JSONTextAttribute(name=name, val=value))

        elif isinstance(value, list):
            vec_attributes.append(JSONVecAttribute(name=name, val=value))

        else:
            raise UnsupportedAttributeTypeError(name, value)

    return JSONAttributes(
        boolean=boolean_attributes, num=num_attributes, text=text_attributes, vec=vec_attributes
    )


class UnsupportedAttributeTypeError(TypeError):
    def __init__(self, attribute_name: str, attribute_value: object) -> None:
        super().__init__(
            f"{attribute_value.__class__.__name__} of attribute {attribute_name} "
            "is not a supported attribute type"
        )
