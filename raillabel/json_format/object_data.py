# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import BaseModel

from .bbox import JSONBbox
from .cuboid import JSONCuboid
from .poly2d import JSONPoly2d
from .poly3d import JSONPoly3d
from .vec import JSONVec


class JSONObjectData(BaseModel):
    """Container of annotations of an object in a frame."""

    bbox: list[JSONBbox] | None
    cuboid: list[JSONCuboid] | None
    poly2d: list[JSONPoly2d] | None
    poly3d: list[JSONPoly3d] | None
    vec: list[JSONVec] | None
