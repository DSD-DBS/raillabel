# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from .attributes import JSONAttributes


class JSONPoly2d(BaseModel):
    """A 2D polyline defined as a sequence of 2D points."""

    name: str
    """This is a string encoding the name of this object data. It is used as index inside the
    corresponding object data pointers."""

    val: list[float | str]
    "List of numerical values of the polyline, according to its mode."

    closed: bool
    """A boolean that defines whether the polyline is closed or not. In case it is closed, it is
    assumed that the last point of the sequence is connected with the first one."""

    mode: Literal["MODE_POLY2D_ABSOLUTE"]
    """Mode of the polyline describes how the points should be arranged in the images.
    MODE_POLY2D_ABSOLUTE means that any point defined by an x-value followed by a y-value is the
    absolute position."""

    coordinate_system: str | None
    "Name of the coordinate system in respect of which this object data is expressed."

    uid: UUID | None
    "This is a string encoding the Universal Unique identifyer of the annotation."

    attributes: JSONAttributes | None