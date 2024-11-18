# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

from ._json_format_base import _JSONFormatBase
from .attributes import JSONAttributes


class JSONBbox(_JSONFormatBase):
    """A 2D bounding box is defined as a 4-dimensional vector [x, y, w, h].

    [x, y] is the center of the bounding box and [w, h] represent the width (horizontal,
    x-coordinate dimension) and height (vertical, y-coordinate dimension), respectively.
    """

    name: str
    """This is a string encoding the name of this object data. It is used as index inside the
    corresponding object data pointers."""

    val: tuple[float, float, float, float]
    "The array of 4 values that define the [x, y, w, h] values of the bbox."

    coordinate_system: str
    "Name of the coordinate system in respect of which this object data is expressed."

    uid: UUID | None = None
    "This is a string encoding the Universal Unique identifyer of the annotation."

    attributes: JSONAttributes | None = None
