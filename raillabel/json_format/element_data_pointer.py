# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .frame_interval import JSONFrameInterval


class JSONElementDataPointer(BaseModel):
    """A pointer to element data of elements.

    It is indexed by 'name', and containing information about the element data type, for example,
    bounding box, cuboid, and the frame intervals in which this element_data exists within an
    element. That means, these pointers can be used to explore element data dynamic information
    within the JSON content.
    """

    attribute_pointers: dict[str, Literal["num", "text", "boolean", "vec"]]
    frame_intervals: list[JSONFrameInterval]
    type: Literal["bbox", "num", "poly2d", "poly3d", "cuboid", "vec"]
