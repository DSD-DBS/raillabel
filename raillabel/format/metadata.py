# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Metadata:
    """Container for metadata information about the scene itself.

    Parameters
    ----------
    schema_version: str
        Version number of the raillabel schema this annotation object follows.
    annotator: str, optional
        Name or description of the annotator that created the annotations. Default is None.
    comment: str, optional
        Additional information or description about the annotation content. Default is None.
    file_version: str, optional
        Version number of the raillabel annotation content. Default is None.
    name: str, optional
        Name of the raillabel annotation content. Default is None.
    tagged_file: str, optional
        Directory with the exported data (e.g. images, point clouds). Default is None.
    devkit_version: str, optional
        Version of the raillabel-devkit, that last exported the scene.
    """

    schema_version: str
    annotator: str = None
    comment: str = None
    file_version: str = None
    name: str = None
    tagged_file: str = None
    exporter_version: str = None

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

        if self.file_version is not None:
            dict_repr["file_version"] = str(self.file_version)

        if self.name is not None:
            dict_repr["name"] = str(self.name)

        if self.tagged_file is not None:
            dict_repr["tagged_file"] = str(self.tagged_file)

        if self.exporter_version is not None:
            dict_repr["exporter_version"] = str(self.exporter_version)

        return dict_repr
