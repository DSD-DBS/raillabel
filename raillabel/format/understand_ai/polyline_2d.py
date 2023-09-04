# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass
from uuid import UUID

from ._annotation import _Annotation
from .sensor_reference import SensorReference


@dataclass
class Polyline2d(_Annotation):
    """A 2d polyline.

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
    points: list[tuple[float, float]]
        2d points belonging to the polyline.
    """

    points: t.List[t.Tuple[float, float]]

    OPENLABEL_ID = "poly2d"

    @classmethod
    def fromdict(cls, data_dict: t.Dict) -> "Polyline2d":
        """Generate a Polyline2d from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        Polyline2d
            Converted 2d polyline.
        """

        return Polyline2d(
            id=UUID(data_dict["id"]),
            object_id=UUID(data_dict["objectId"]),
            class_name=data_dict["className"],
            attributes=data_dict["attributes"],
            sensor=SensorReference.fromdict(data_dict["sensor"]),
            points=[(p[0], p[1]) for p in data_dict["geometry"]["points"]],
        )

    def to_raillabel(self) -> t.Tuple[dict, str, str, dict]:
        """Convert to a raillabel compatible dict.

        Returns
        -------
        annotation: dict
            Dictionary valid for the raillabel schema.
        object_id: str
            Friendly identifier of the object this sensor belongs to.
        class_name: str
            Friendly identifier of the class the annotated object belongs to.
        sensor_reference: dict
            Dictionary of the sensor reference.
        """

        polyline = super().to_raillabel()
        polyline[0]["closed"] = False
        polyline[0]["mode"] = "MODE_POLY2D_ABSOLUTE"

        return polyline

    def _val_to_raillabel(self) -> t.List[float]:
        return [coordinate for point in self.points for coordinate in point]
