# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from .attributes import JSONAttributes


class JSONNum(BaseModel):
    """A number."""

    name: str
    """This is a string encoding the name of this object data. It is used as index inside the
    corresponding object data pointers."""

    val: list[int]
    "The numerical value of the number."

    coordinate_system: str | None
    "Name of the coordinate system in respect of which this object data is expressed."

    uid: UUID | None
    "This is a string encoding the Universal Unique identifyer of the annotation."

    attributes: JSONAttributes | None