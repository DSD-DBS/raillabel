# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass
from importlib import metadata as importlib_metadata


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
    annotator: t.Optional[str] = None
    comment: t.Optional[str] = None
    exporter_version: t.Optional[str] = None
    file_version: t.Optional[str] = None
    name: t.Optional[str] = None
    subschema_version: t.Optional[str] = None
    tagged_file: t.Optional[str] = None

    @classmethod
    def fromdict(cls, data_dict: dict, subschema_version: t.Optional[str] = None) -> "Metadata":
        """Generate a Metadata object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data. Additional (non-defined)
            arguments can be set and will be added as properties to Metadata.
        subschema_version: str, optional
            Version of the RailLabel subschema

        Returns
        -------
        metadata: Metadata
            Converted metadata.
        """

        metadata = Metadata(
            schema_version=data_dict["schema_version"],
            subschema_version=subschema_version,
            exporter_version=cls._collect_exporter_version(),
        )

        return cls._set_additional_attributes(metadata, data_dict)

    def asdict(self) -> dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this class instance.
        """

        return self._remove_empty_fields(vars(self))

    @classmethod
    def _collect_exporter_version(cls) -> t.Optional[str]:

        try:
            exporter_version = importlib_metadata.version("raillabel")
        except importlib_metadata.PackageNotFoundError:
            return None

        version_number_length = len(exporter_version) - len(exporter_version.split(".")[-1])
        return exporter_version[: version_number_length - 1]

    @classmethod
    def _set_additional_attributes(cls, metadata: "Metadata", data_dict: dict) -> "Metadata":

        PRESET_KEYS = ["schema_version", "subschema_version", "exporter_version"]

        for key, value in data_dict.items():
            if key in PRESET_KEYS:
                continue

            is_key_a_valid_python_attribute = isinstance(key, str) and key.isidentifier()

            if not is_key_a_valid_python_attribute:
                raise KeyError(f"'{key}' is not a valid python attribute")

            setattr(metadata, key, value)

        return metadata

    def _remove_empty_fields(self, dict_repr: dict) -> dict:
        """Remove empty fields from a dictionary."""
        return {k: v for k, v in dict_repr.items() if v is not None}
