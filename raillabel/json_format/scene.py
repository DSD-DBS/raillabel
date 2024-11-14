# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

from ._json_format_base import _JSONFormatBase
from .coordinate_system import JSONCoordinateSystem
from .frame import JSONFrame
from .frame_interval import JSONFrameInterval
from .metadata import JSONMetadata
from .object import JSONObject
from .stream_camera import JSONStreamCamera
from .stream_other import JSONStreamOther
from .stream_radar import JSONStreamRadar


class JSONScene(_JSONFormatBase):
    """Root RailLabel object."""

    openlabel: JSONSceneContent


class JSONSceneContent(_JSONFormatBase):
    """Container of all scene content."""

    metadata: JSONMetadata
    coordinate_systems: dict[str, JSONCoordinateSystem] | None = None
    streams: dict[str, JSONStreamCamera | JSONStreamOther | JSONStreamRadar] | None = None
    objects: dict[UUID, JSONObject] | None = None
    frames: dict[int, JSONFrame] | None = None
    frame_intervals: list[JSONFrameInterval] | None = None
