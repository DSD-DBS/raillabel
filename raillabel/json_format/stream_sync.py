# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class JSONStreamSync(BaseModel):
    """Syncronization information of a stream in a frame."""

    stream_properties: JSONStreamSyncProperties
    uri: str | None


class JSONStreamSyncProperties(BaseModel):
    """The sync information."""

    sync: JSONStreamSyncTimestamp


class JSONStreamSyncTimestamp(BaseModel):
    """The timestamp of a stream sync."""

    timestamp: Decimal | str
