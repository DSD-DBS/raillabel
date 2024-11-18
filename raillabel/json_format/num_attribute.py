# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ._json_format_base import _JSONFormatBase


class JSONNumAttribute(_JSONFormatBase):
    """A number attribute."""

    name: str
    """Friendly identifier describing the attribute. Used to track the attribute throughout
    annotations and frames."""

    val: float
    "The number value."
