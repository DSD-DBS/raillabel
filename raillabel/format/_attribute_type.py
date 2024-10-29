# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum


class AttributeType(Enum):
    """Enum of all valid RailLabel attribute types."""

    TEXT = "text"
    NUM = "num"
    BOOLEAN = "boolean"
    VEC = "vec"

    @classmethod
    def from_value(cls, attribute_value_class: type) -> AttributeType:
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
        UnsupportedAttributeTypeError
            if attribute value class does not correspond to an Attribute Type.

        """
        if attribute_value_class == str:
            return AttributeType.TEXT

        if attribute_value_class in [float, int]:
            return AttributeType.NUM

        if attribute_value_class == bool:
            return AttributeType.BOOLEAN

        if attribute_value_class in [list, tuple]:
            return AttributeType.VEC

        raise UnsupportedAttributeTypeError(attribute_value_class)


class UnsupportedAttributeTypeError(ValueError):
    def __init__(self, attribute_value_class: type) -> None:
        super().__init__(
            f"Type {attribute_value_class} does not correspond to a valid RailLabel attribute "
            "type. Supported types are str, float, int, bool, list, tuple."
        )
