# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from decimal import Decimal

from ._json_format_base import _JSONFormatBase


class JSONStreamSync(_JSONFormatBase):
    """Syncronization information of a stream in a frame."""

    stream_properties: JSONStreamSyncProperties
    uri: str | None = None


class JSONStreamSyncProperties(_JSONFormatBase):
    """The sync information."""

    sync: JSONStreamSyncTimestamp


class JSONStreamSyncTimestamp(_JSONFormatBase):
    """The timestamp of a stream sync."""

    timestamp: Decimal | str
