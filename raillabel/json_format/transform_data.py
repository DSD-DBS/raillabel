# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import BaseModel


class JSONTransformData(BaseModel, extra="forbid"):
    """The translation and rotation of one coordinate system to another."""

    translation: tuple[float, float, float]
    "List of 4 values encoding a quaternion (x, y, z, w)."

    quaternion: tuple[float, float, float, float]
    "List of 3 values encoding the translation vector (x, y, z)"
