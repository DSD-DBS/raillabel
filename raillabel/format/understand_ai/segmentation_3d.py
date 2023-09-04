# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass
from uuid import UUID

from ._annotation import _Annotation
from .sensor_reference import SensorReference


@dataclass
class Segmentation3d(_Annotation):
    """The 3D segmentation of a lidar pointcloud.

    Parameters
    ----------
    id: uuid.UUID
        Unique identifier of the annotation.
    object_id: uuid.UUID
        Unique identifier of the object this annotation refers to. Used for tracking.
    class_name: str
        Name of the class this annotation belongs to.
    attributes: dict[str, str or list]
        Key value pairs of attributes with the keys beeing the friendly identifier of the
        attribute and the value beeing the attribute value.
    sensor: raillabel.format.understand_ai.SensorReference
        Information about the sensor this annotation is labeled in.
    associated_points: list[int]
        List of point indices of the lidar pointcloud.
    number_of_points: int
        Total number of points in the associated_points.
    """

    associated_points: t.List[int]
    number_of_points: int

    OPENLABEL_ID = "vec"

    @classmethod
    def fromdict(cls, data_dict: t.Dict) -> "Segmentation3d":
        """Generate a Segmentation3d from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        Segmentation3d
            Converted 3d segmentation.
        """

        return Segmentation3d(
            id=UUID(data_dict["id"]),
            object_id=UUID(data_dict["objectId"]),
            class_name=data_dict["className"],
            attributes=data_dict["attributes"],
            sensor=SensorReference.fromdict(data_dict["sensor"]),
            associated_points=data_dict["geometry"]["associatedPoints"],
            number_of_points=data_dict["geometry"]["numberOfPointsInBox"],
        )

    def _val_to_raillabel(self) -> list:
        return self.associated_points
