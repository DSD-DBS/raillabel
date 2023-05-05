# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from ._annotation import _Annotation


@dataclass
class Num(_Annotation):
    """A number.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier of the annotation.
    name: str
        Human readable name describing the annotation.
    val: int or float
        This is the value of the number object.
    attributes: dict, optional
        Attributes of the annotation. Dict keys are the uid str of the attribute, values are the
        attribute values. Default is {}.
    sensor: raillabel.format.CoordinateSystem, optional
        A reference to the sensor, this value is represented in. Default is None.
    """

    val: t.Union[int, float] = None

    OPENLABEL_ID = "num"
    _REQ_FIELDS = ["val"]

    @classmethod
    def fromdict(self, data_dict: dict, sensors: dict) -> "Num":
        """Generate a Num object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        sensors: dict
            Dictionary containing all sensors for the scene.

        Returns
        -------
        annotation: Num
            Converted annotation.
        """

        return Num(
            uid=str(data_dict["uid"]),
            name=str(data_dict["name"]),
            val=data_dict["val"],
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

        dict_repr["val"] = self.val

        dict_repr.update(self._annotation_optional_fields_asdict())

        return dict_repr
