# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ._json_format_base import _JSONFormatBase
from .element_data_pointer import JSONElementDataPointer
from .frame_interval import JSONFrameInterval


class JSONObject(_JSONFormatBase):
    """An object is the main type of annotation element.

    Object is designed to represent spatiotemporal entities, such as physical objects in the real
    world. Objects shall have a name and type. Objects may have static and dynamic data. Objects
    are the only type of elements that may have geometric data, such as bounding boxes, cuboids,
    polylines, images, etc.
    """

    name: str
    "Name of the object. It is a friendly name and not used for indexing."

    type: str
    "The type of an object defines the class the object corresponds to."

    frame_intervals: list[JSONFrameInterval] | None = None
    "The array of frame intervals where this object exists or is defined."

    object_data_pointers: dict[str, JSONElementDataPointer] | None = None
