# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass
from uuid import UUID

from ._annotation import _Annotation
from .sensor_reference import SensorReference


@dataclass
class BoundingBox2d(_Annotation):
    """A 2d bounding box.

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
    x_min: float
        Left corner of the bounding box in pixels.
    y_min: float
        Top corner of the bounding box in pixels.
    x_max: float
        Right corner of the bounding box in pixels.
    y_max: float
        Bottom corner of the bounding box in pixels.
    """

    x_min: float
    y_min: float
    x_max: float
    y_max: float

    OPENLABEL_ID = "bbox"

    @classmethod
    def fromdict(cls, data_dict: t.Dict) -> "BoundingBox2d":
        """Generate a BoundingBox2d from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        BoundingBox2d
            Converted 2d bounding box.
        """

        return BoundingBox2d(
            id=UUID(data_dict["id"]),
            object_id=UUID(data_dict["objectId"]),
            class_name=data_dict["className"],
            x_min=data_dict["geometry"]["xMin"],
            y_min=data_dict["geometry"]["yMin"],
            x_max=data_dict["geometry"]["xMax"],
            y_max=data_dict["geometry"]["yMax"],
            attributes=data_dict["attributes"],
            sensor=SensorReference.fromdict(data_dict["sensor"]),
        )

    def _val_to_raillabel(self) -> list:
        return [
            (self.x_max + self.x_min) / 2,
            (self.y_max + self.y_min) / 2,
            abs(self.x_max - self.x_min),
            abs(self.y_max - self.y_min),
        ]
