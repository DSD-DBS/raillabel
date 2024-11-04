# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from ._attribute_type import AttributeType
from .frame_interval import FrameInterval


@dataclass
class ElementDataPointer:
    """Container of pointers for annotations indexed by the "name" property.

    Used for indexing annotations for easy referencing without loading all of them.

    Parameters
    ----------
    uid: str
        Unique identifier of the ElementDataPointer assembled using a specific schema.
    frame_intervals: list[raillabel.format.FrameInterval]
        Frame intervals, this element data pointer is contained in.
    attribute_pointers: dict[str, raillabel.util._attribute_type.AttributeType]
        References of attributes contained in the referenced annotations with attribute type.

    Properties (read-only)
    ----------------------
    uid: str
        Unique identifier of the ElementDataPointer built from the attributes.

    """

    uid: str
    frame_intervals: list[FrameInterval]
    attribute_pointers: dict[str, AttributeType]
