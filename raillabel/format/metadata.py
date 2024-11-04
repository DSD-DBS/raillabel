# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Metadata:
    """Container for metadata information about the scene itself.

    As the OpenLABEL metadata object accepts additional properties, so does this class. Any
    properties present in the JSON will be added to the Metadata() object when read through
    Metadata.fromdict(). Conversely, all attributes from the Metadata() object will be stored
    into the JSON when using Metadata.asdict(). You can therefore just add attributes to the
    Python object and have them stored.
    Example:
        m = Metadata.fromdict(
            {
                "schema_version": "1.0.0",
                "some_additional_property": "Some Value"
            }
        )
        m.another_additional_property = "Another Value"
        m.asdict()
        -> {
            "schema_version": "1.0.0",
            "some_additional_property": "Some Value",
            "another_additional_property": "Another Value"
        }

    Parameters
    ----------
    schema_version: str
        Version number of the OpenLABEL schema this annotation object follows.
    annotator: str, optional
        Name or description of the annotator that created the annotations. Default is None.
    comment: str, optional
        Additional information or description about the annotation content. Default is None.
    exporter_version: str, optional
        Version of the raillabel-devkit, that last exported the scene. Default is None.
    file_version: str, optional
        Version number of the raillabel annotation content. Default is None.
    name: str, optional
        Name of the raillabel annotation content. Default is None.
    subschema_version: str, optional
        Version number of the RailLabel schema this annotation object follows. Default is None.
    tagged_file: str, optional
        Directory with the exported data_dict (e.g. images, point clouds). Default is None.

    """

    schema_version: str
    annotator: str | None = None
    comment: str | None = None
    exporter_version: str | None = None
    file_version: str | None = None
    name: str | None = None
    subschema_version: str | None = None
    tagged_file: str | None = None
