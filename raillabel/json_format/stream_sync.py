# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class JSONStreamSync(BaseModel, extra="forbid"):
    """Syncronization information of a stream in a frame."""

    stream_properties: JSONStreamSyncProperties
    uri: str | None = None


class JSONStreamSyncProperties(BaseModel, extra="forbid"):
    """The sync information."""

    sync: JSONStreamSyncTimestamp


class JSONStreamSyncTimestamp(BaseModel, extra="forbid"):
    """The timestamp of a stream sync."""

    timestamp: Decimal | str
