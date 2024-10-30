# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .transform_data import JSONTransformData


class JSONCoordinateSystem(BaseModel):
    """A 3D reference frame."""

    children: list[str]
    "List of children of this coordinate system."

    parent: Literal["base", ""]
    "This is the string UID of the parent coordinate system this coordinate system is referring to."

    pose_wrt_parent: JSONTransformData
    "The transformation with regards to the parent coordinate system."

    type: Literal["sensor", "local"]
    """This is a string that describes the type of the coordinate system, for example, 'local',
    'geo')."""
