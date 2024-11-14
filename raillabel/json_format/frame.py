# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from .num import JSONNum
from .object_data import JSONObjectData
from .stream_sync import JSONStreamSync


class JSONFrame(BaseModel, extra="forbid"):
    """A frame is a container of dynamic, timewise, information."""

    frame_properties: JSONFrameProperties | None = None
    "Container of frame information other than annotations."

    objects: dict[UUID, JSONObjectData] | None = None
    """This is a JSON object that contains dynamic information on RailLabel objects. Object keys are
    strings containing 32 bytes UUIDs. Object values contain an 'object_data' JSON object."""


class JSONFrameProperties(BaseModel, extra="forbid"):
    """Container of frame information other than annotations."""

    timestamp: Decimal | str | None = None
    """The timestamp indicates a time instant as a UTC string or numerical value to describe this
    frame."""

    streams: dict[str, JSONStreamSync] | None = None
    """Stream timestamps for synchronization."""

    frame_data: JSONFrameData | None = None
    "Additional data to describe attributes of the frame (like GPS position)."


class JSONFrameData(BaseModel, extra="forbid"):
    """Additional data to describe attributes of the frame (like GPS position)."""

    num: list[JSONNum] | None = None
    "List of 'num' that describe this frame."
