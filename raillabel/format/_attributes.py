# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from raillabel.json_format import JSONAttributes


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
