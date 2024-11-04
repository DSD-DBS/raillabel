# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from .attributes import JSONAttributes


class JSONCuboid(BaseModel):
    """A cuboid or 3D bounding box.

    It is defined by the position of its center, the rotation in 3D, and its dimensions.
    """

    name: str
    """This is a string encoding the name of this object data. It is used as index inside the
    corresponding object data pointers."""

    val: tuple[float, float, float, float, float, float, float, float, float, float]
    """List of values encoding the position, rotation and dimensions. It is
    (x, y, z, qx, qy, qz, qw, sx, sy, sz) where (x, y, z) encodes the position, (qx, qy, qz, qw)
    encodes the quaternion that encode the rotation, and (sx, sy, sz) are the dimensions of the
    cuboid in its object coordinate system"""

    coordinate_system: str | None = None
    "Name of the coordinate system in respect of which this object data is expressed."

    uid: UUID | None = None
    "This is a string encoding the Universal Unique identifyer of the annotation."

    attributes: JSONAttributes | None = None
