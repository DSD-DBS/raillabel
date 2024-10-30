# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import BaseModel


class JSONTransformData(BaseModel):
    """The translation and rotation of one coordinate system to another."""

    translation: tuple[float, float, float]
    quaternion: tuple[float, float, float, float]
