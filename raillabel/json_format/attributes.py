# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ._json_format_base import _JSONFormatBase
from .boolean_attribute import JSONBooleanAttribute
from .num_attribute import JSONNumAttribute
from .text_attribute import JSONTextAttribute
from .vec_attribute import JSONVecAttribute


class JSONAttributes(_JSONFormatBase):
    """Attributes is the alias of element data that can be nested inside geometric object data.

    For example, a certain bounding box can have attributes related to its score, visibility, etc.
    These values can be nested inside the bounding box as attributes.
    """

    boolean: list[JSONBooleanAttribute] | None = None
    num: list[JSONNumAttribute] | None = None
    text: list[JSONTextAttribute] | None = None
    vec: list[JSONVecAttribute] | None = None
