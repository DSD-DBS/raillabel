# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from ._json_format_base import _JSONFormatBase
from .transform_data import JSONTransformData


class JSONCoordinateSystem(_JSONFormatBase):
    """A 3D reference frame."""

    parent: Literal["base", ""]
    "This is the string UID of the parent coordinate system this coordinate system is referring to."

    type: Literal["sensor", "local"]
    """This is a string that describes the type of the coordinate system, for example, 'local',
    'geo')."""

    pose_wrt_parent: JSONTransformData | None = None
    "The transformation with regards to the parent coordinate system."

    children: list[str] | None = None
    "List of children of this coordinate system."
