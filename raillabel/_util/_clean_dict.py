# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0


def _clean_dict(input_dict: dict) -> dict:
    """Remove all fields from a dict that are None or have a length of 0."""

    empty_keys = []
    for key, value in input_dict.items():

        is_field_empty = value is None or (hasattr(value, "__len__") and len(value) == 0)

        if is_field_empty:
            empty_keys.append(key)

    for key in empty_keys:
        del input_dict[key]

    return input_dict
