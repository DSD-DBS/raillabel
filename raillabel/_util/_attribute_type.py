# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from enum import Enum


class AttributeType(Enum):
    """Enum of all valid RailLabel attribute types."""

    TEXT = "text"
    NUM = "num"
    BOOLEAN = "boolean"
    VEC = "vec"

    @classmethod
    def from_value(cls, attribute_value_class: t.Type) -> "AttributeType":
        """Return AttributeType based on class of attribute value.

        Parameters
        ----------
        attribute_value_class: type
            Class of the attribute value. Can be gathered by calling type()-function.

        Returns
        -------
        AttributeType
            Corresponding AttributeType.

        Raises
        ------
        ValueError
            if attribute value class does not correspond to an Attribute Type.
        """

        if attribute_value_class == str:
            return AttributeType.TEXT

        elif attribute_value_class in [float, int]:
            return AttributeType.NUM

        elif attribute_value_class == bool:
            return AttributeType.BOOLEAN

        elif attribute_value_class in [list, tuple]:
            return AttributeType.VEC

        else:
            raise ValueError(
                f"Type {attribute_value_class} does not correspond to a valid RailLabel attribute "
                + "type. Supported types are str, float, int, bool, list, tuple."
            )
