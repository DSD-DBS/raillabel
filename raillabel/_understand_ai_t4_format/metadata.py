# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Metadata:
    """Container for metadata information about the scene itself.

    Parameters
    ----------
    clip_id: str
        Identifier of the scene for internal purposes.
    external_clip_id: str
        Identifier of the scene for external purposes.
    project_id: str
        Identifier of the annotation project.
    export_time: str
        Timestamp of the export in the format 'YYYY-MM-DD hh:mm UTC'.
    exporter_version: str
        Version of the Understand.AI-exporter.
    coordinate_system_3d: str
    coordinate_system_reference: str
    folder_name: str
        Directory with the exported reference data (e.g. images, point clouds).
    """

    clip_id: str
    external_clip_id: str
    project_id: str
    export_time: str
    exporter_version: str
    coordinate_system_3d: str
    coordinate_system_reference: str
    folder_name: str

    @classmethod
    def fromdict(cls, data_dict: dict) -> "Metadata":
        """Generate a Metadata from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        metadata: Metadata
            Converted metadata.
        """

        return Metadata(
            clip_id=data_dict["clip_id"],
            external_clip_id=data_dict["external_clip_id"],
            project_id=data_dict["project_id"],
            export_time=data_dict["export_time"],
            exporter_version=data_dict["exporter_version"],
            coordinate_system_3d=data_dict["coordinate_system_3d"],
            coordinate_system_reference=data_dict["coordinate_system_reference"],
            folder_name=data_dict["folder_name"],
        )