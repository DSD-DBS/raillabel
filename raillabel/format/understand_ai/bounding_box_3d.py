# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass
from uuid import UUID

from ._annotation import _Annotation
from .point_3d import Point3d
from .quaternion import Quaternion
from .sensor_reference import SensorReference
from .size_3d import Size3d


@dataclass
class BoundingBox3d(_Annotation):
    """A 3d bounding box.

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
    center: raillabel.format.understand_ai.Point3d
        Center position of the bounding box.
    size: raillabel.format.understand_ai.Size3d
        3d size of the bounding box.
    quaternion: raillabel.format.understand_ai.Quaternion
        Rotation quaternion of the bounding box.
    """

    center: Point3d
    size: Size3d
    quaternion: Quaternion

    OPENLABEL_ID = "cuboid"

    @classmethod
    def fromdict(cls, data_dict: t.Dict) -> "BoundingBox3d":
        """Generate a BoundingBox3d from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        BoundingBox3d
            Converted 3d bounding box.
        """

        return BoundingBox3d(
            id=UUID(data_dict["id"]),
            object_id=UUID(data_dict["objectId"]),
            class_name=data_dict["className"],
            center=Point3d.fromdict(data_dict["geometry"]["center"]),
            size=Size3d.fromdict(data_dict["geometry"]["size"]),
            quaternion=Quaternion.fromdict(data_dict["geometry"]["quaternion"]),
            attributes=data_dict["attributes"],
            sensor=SensorReference.fromdict(data_dict["sensor"]),
        )

    def _val_to_raillabel(self) -> list:
        return [
            float(self.center.x),
            float(self.center.y),
            float(self.center.z),
            float(self.quaternion.x),
            float(self.quaternion.y),
            float(self.quaternion.z),
            float(self.quaternion.w),
            float(self.size.width),
            float(self.size.length),
            float(self.size.height),
        ]
