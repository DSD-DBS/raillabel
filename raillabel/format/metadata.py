# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.json_format import JSONMetadata


@dataclass
class Metadata:
    """Container for metadata information about the scene itself."""

    schema_version: str
    "Version number of the OpenLABEL schema this annotation object follows."

    annotator: str | None = None
    "Name or description of the annotator that created the annotations."

    comment: str | None = None
    "Additional information or description about the annotation content."

    exporter_version: str | None = None
    "Version of the raillabel-devkit, that last exported the scene."

    file_version: str | None = None
    "Version number of the raillabel annotation content."

    name: str | None = None
    "Name of the raillabel annotation content."

    subschema_version: str | None = None
    "Version number of the RailLabel schema this annotation object follows."

    tagged_file: str | None = None
    "Directory with the exported data_dict (e.g. images, point clouds)."

    @classmethod
    def from_json(cls, json: JSONMetadata) -> Metadata:
        """Construct an instant of this class from RailLabel JSON data."""
        metadata = Metadata(
            schema_version=json.schema_version,
            name=json.name,
            subschema_version=json.subschema_version,
            exporter_version=json.exporter_version,
            file_version=json.file_version,
            tagged_file=json.tagged_file,
            annotator=json.annotator,
            comment=json.comment,
        )

        if json.model_extra is not None:
            for extra_field, extra_value in json.model_extra.items():
                setattr(metadata, extra_field, extra_value)

        return metadata

    def to_json(self) -> JSONMetadata:
        """Export this object into the RailLabel JSON format."""
        return JSONMetadata(**dict(vars(self)))
