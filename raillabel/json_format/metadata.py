# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class JSONMetadata(BaseModel):
    """Metadata about the annotation file itself."""

    schema_version: Literal["1.0.0"]
    "Version number of the OpenLABEL schema this annotation file follows."

    name: str | None
    "Name of the OpenLABEL annotation content."

    subschema_version: str | None
    "Version number of the RailLabel subschema this annotation file follows."

    exporter_version: str | None
    "Version identifyer of the exporter software."

    file_version: str | None
    "Version number of the OpenLABEL annotation content."

    tagged_file: str | None
    "File name or URI of the data file being tagged."

    comment: str | None
    "Additional information or description about the annotation content."
