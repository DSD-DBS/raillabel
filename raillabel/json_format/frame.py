# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from .num import JSONNum
from .object_data import JSONObjectData
from .stream_sync import JSONStreamSync


class JSONFrame(BaseModel):
    """A frame interval defines a starting and ending frame number as a closed interval.

    That means the interval includes the limit frame numbers.
    """

    frame_properties: JSONFrameProperties | None
    "Container of frame information other than annotations."

    objects: dict[UUID, JSONObjectData]
    """This is a JSON object that contains dynamic information on RailLabel objects. Object keys are
    strings containing 32 bytes UUIDs. Object values contain an 'object_data' JSON object."""


class JSONFrameProperties(BaseModel):
    """Container of frame information other than annotations."""

    timestamp: Decimal | str | None
    """The timestamp indicates a time instant as a UTC string or numerical value to describe this
    frame."""

    streams: dict[str, JSONStreamSync] | None
    """Stream timestamps for synchronization."""

    frame_data: JSONFrameData | None
    "Additional data to describe attributes of the frame (like GPS position)."


class JSONFrameData(BaseModel):
    """Additional data to describe attributes of the frame (like GPS position)."""

    num: list[JSONNum] | None
    "List of 'num' that describe this frame."
