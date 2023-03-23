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
        """Generate a Metadata from a dictionary in the OpenLABEL format.

        Parameters
        ----------
        data_dict: dict
            OpenLABEL format dictionary containing the data_dict.
        subschema_version: str, optional
            Version of the RailLabel subschema

        Returns
        -------
        metadata: Metadata
            Converted metadata.
        warnings: list of str
            List of non-critical errors, that have occurred during the conversion.
        """

        metadata = Metadata(schema_version=data_dict["schema_version"])

        if subschema_version is not None:
            metadata.subschema_version = subschema_version

        if "annotator" in data_dict:
            metadata.annotator = data_dict["annotator"]

        if "file_version" in data_dict:
            metadata.file_version = data_dict["file_version"]

        if "name" in data_dict:
            metadata.name = data_dict["name"]

        if "tagged_file" in data_dict:
            metadata.tagged_file = data_dict["tagged_file"]

        if "comment" in data_dict:
            metadata.comment = data_dict["comment"]

        try:
            metadata.exporter_version = importlib_metadata.version("pyraillabel").split("+")[0]
        except importlib_metadata.PackageNotFoundError:
            pass

        return metadata

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
