# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from ._json_format_base import _JSONFormatBase
from .frame_interval import JSONFrameInterval


class JSONElementDataPointer(_JSONFormatBase):
    """A pointer to element data of elements.

    It is indexed by 'name', and containing information about the element data type, for example,
    bounding box, cuboid, and the frame intervals in which this element_data exists within an
    element. That means, these pointers can be used to explore element data dynamic information
    within the JSON content.
    """

    attribute_pointers: dict[str, Literal["num", "text", "boolean", "vec"]]
    """This is a JSON object which contains pointers to the attributes of the element data pointed by
    this pointer. The attributes pointer keys shall be the 'name' of the attribute of the element
    data this pointer points to."""

    frame_intervals: list[JSONFrameInterval]
    "List of frame intervals of the element data pointed by this pointer."

    type: Literal["bbox", "num", "poly2d", "poly3d", "cuboid", "vec"]
    "Type of the element data pointed by this pointer."
