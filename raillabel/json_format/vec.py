# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal
from uuid import UUID

from ._json_format_base import _JSONFormatBase
from .attributes import JSONAttributes


class JSONVec(_JSONFormatBase):
    """A vector (list) of numbers."""

    name: str
    """This is a string encoding the name of this object data. It is used as index inside the
    corresponding object data pointers."""

    val: list[float]
    "The numerical values of the vector (list) of numbers."

    coordinate_system: str
    "Name of the coordinate system in respect of which this object data is expressed."

    uid: UUID | None = None
    "This is a string encoding the Universal Unique identifyer of the annotation."

    type: Literal["values", "range"] | None = None
    """This attribute specifies whether the vector shall be considered as a descriptor of individual
    values or as a definition of a range."""

    attributes: JSONAttributes | None = None
