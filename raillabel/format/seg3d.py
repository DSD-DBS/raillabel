# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from ._annotation import _Annotation


@dataclass
class Seg3d(_Annotation):
    """The 3D segmentation of a lidar pointcloud.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier of the annotation.
    name: str
        Human readable name describing the annotation.
    point_ids: list of int
        The list of point indices.
    attributes: dict, optional
        Attributes of the annotation. Default is {}.
    sensor: raillabel.format.CoordinateSystem, optional
        The sensor, this annotation is labeled in. Default is None.
    """

    point_ids: t.List[int] = None

    OPENLABEL_ID = "vec"
    _REQ_FIELDS = ["point_ids"]

    @classmethod
    def fromdict(
        self,
        data_dict: dict,
        sensors: dict,
    ) -> "Seg3d":
        """Generate a Seg3d object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        sensors: dict
            Dictionary containing all sensors for the scene.

        Returns
        -------
        annotation: Seg3d
            Converted annotation.
        """

        return Seg3d(
            uid=str(data_dict["uid"]),
            name=str(data_dict["name"]),
            point_ids=data_dict["val"],
            sensor=self._coordinate_system_fromdict(data_dict, sensors),
            attributes=self._attributes_fromdict(data_dict),
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
