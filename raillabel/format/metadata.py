# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass
from importlib import metadata as importlib_metadata


@dataclass
class Metadata:
    """Container for metadata information about the scene itself.

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

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.
        """

        dict_repr = {"schema_version": str(self.schema_version)}

        if self.annotator is not None:
            dict_repr["annotator"] = str(self.annotator)

        if self.comment is not None:
            dict_repr["comment"] = str(self.comment)

        if self.exporter_version is not None:
            dict_repr["exporter_version"] = str(self.exporter_version)

        if self.file_version is not None:
            dict_repr["file_version"] = str(self.file_version)

        if self.name is not None:
            dict_repr["name"] = str(self.name)

        if self.subschema_version is not None:
            dict_repr["subschema_version"] = str(self.subschema_version)

        if self.tagged_file is not None:
            dict_repr["tagged_file"] = str(self.tagged_file)

        return dict_repr

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
