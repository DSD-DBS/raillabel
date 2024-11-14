# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import BaseModel


class JSONTextAttribute(BaseModel, extra="forbid"):
    """A text attribute."""

    name: str
    """Friendly identifier describing the attribute. Used to track the attribute throughout
    annotations and frames."""

    val: str
    "The text value."
