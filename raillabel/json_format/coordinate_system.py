# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .transform_data import JSONTransformData


class JSONCoordinateSystem(BaseModel):
    """A 3D reference frame."""

    children: list[str]
    parent: Literal["base", ""]
    pose_wrt_parent: JSONTransformData
    type: Literal["sensor", "local"]
