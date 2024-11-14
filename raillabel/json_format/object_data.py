# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import BaseModel

from .bbox import JSONBbox
from .cuboid import JSONCuboid
from .poly2d import JSONPoly2d
from .poly3d import JSONPoly3d
from .vec import JSONVec


class JSONObjectData(BaseModel, extra="forbid"):
    """Container of annotations of an object in a frame."""

    object_data: JSONAnnotations


class JSONAnnotations(BaseModel, extra="forbid"):
    """Container of the annotations by type."""

    bbox: list[JSONBbox] | None = None
    cuboid: list[JSONCuboid] | None = None
    poly2d: list[JSONPoly2d] | None = None
    poly3d: list[JSONPoly3d] | None = None
    vec: list[JSONVec] | None = None
