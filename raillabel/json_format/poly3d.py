# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

from ._json_format_base import _JSONFormatBase
from .attributes import JSONAttributes


class JSONPoly3d(_JSONFormatBase):
    """A 3D polyline defined as a sequence of 3D points."""

    name: str
    """This is a string encoding the name of this object data. It is used as index inside the
    corresponding object data pointers."""

    val: list[float]
    "List of numerical values of the polyline, according to its mode."

    closed: bool
    """A boolean that defines whether the polyline is closed or not. In case it is closed, it is
    assumed that the last point of the sequence is connected with the first one."""

    coordinate_system: str
    "Name of the coordinate system in respect of which this object data is expressed."

    uid: UUID | None = None
    "This is a string encoding the Universal Unique identifyer of the annotation."

    attributes: JSONAttributes | None = None
