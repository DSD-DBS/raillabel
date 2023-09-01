# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from ._object_annotation import _ObjectAnnotation
from .object import Object


@dataclass
class Seg3d(_ObjectAnnotation):
    """The 3D segmentation of a lidar pointcloud.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier of the annotation.
    point_ids: list of int
        The list of point indices.
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

    point_ids: t.List[int] = None

    OPENLABEL_ID = "vec"
    _REQ_FIELDS = ["point_ids"]

    @classmethod
    def fromdict(cls, data_dict: dict, sensors: dict, object: Object) -> "Seg3d":
        """Generate a Seg3d object from a dict.

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
        annotation: Seg3d
            Converted annotation.
        """

        return Seg3d(
            uid=str(data_dict["uid"]),
            point_ids=data_dict["val"],
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

        dict_repr["val"] = [int(pid) for pid in self.point_ids]

        dict_repr.update(self._annotation_optional_fields_asdict())

        return dict_repr
