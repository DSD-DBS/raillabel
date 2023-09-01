# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from ._object_annotation import _ObjectAnnotation
from .object import Object
from .point3d import Point3d


@dataclass
class Poly3d(_ObjectAnnotation):
    """Sequence of 3D points. Can either be a polygon or polyline.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier for the annotation.
    points: list of raillabel.format.Point3d
        List of the 3d points that make up the polyline.
    closed: bool
        This parameter states, whether the polyline represents a closed shape (a polygon) or an
        open line.
    object: raillabel.format.Object
        A reference to the object, this annotation belongs to.
    sensor: raillabel.format.Sensor, optional
        A reference to the sensor, this annotation is labeled in. Default is None.
    attributes: dict, optional
        Attributes of the annotation. Dict keys are the name str of the attribute, values are the
        attribute values. Default is {}.

    Properties (read-only)
    ----------------------
    name: str
        Name of the annotation used by the VCD player for indexing in the object data pointers.
    """

    points: t.List[Point3d] = None
    closed: bool = None

    OPENLABEL_ID = "poly3d"
    _REQ_FIELDS = ["points", "closed"]

    @classmethod
    def fromdict(cls, data_dict: dict, sensors: dict, object: Object) -> "Poly3d":
        """Generate a Poly3d object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        sensors: dict
            Dictionary containing all sensors for the scene.
        object: raillabel.format.Object
            Object this annotation belongs to.

        Returns
        -------
        annotation: Poly3d
            Converted annotation.
        """

        return Poly3d(
            uid=str(data_dict["uid"]),
            closed=data_dict["closed"],
            points=cls._points_fromdict(data_dict),
            object=object,
            sensor=cls._coordinate_system_fromdict(data_dict, sensors),
            attributes=cls._attributes_fromdict(data_dict),
        )

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

        dict_repr = self._annotation_required_fields_asdict()

        dict_repr["closed"] = bool(self.closed)
        dict_repr["val"] = []
        for point in self.points:
            dict_repr["val"].extend(point.asdict())

        dict_repr.update(self._annotation_optional_fields_asdict())

        return dict_repr

    @classmethod
    def _points_fromdict(cls, data_dict: dict) -> t.List[Point3d]:
        points = []
        for i in range(0, len(data_dict["val"]), 3):
            points.append(
                Point3d(x=data_dict["val"][i], y=data_dict["val"][i + 1], z=data_dict["val"][i + 2])
            )
        return points
