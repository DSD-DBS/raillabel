# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from ..._util._warning import _warning
from .sensor import Sensor


@dataclass
class Num:
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
    sensor: raillabel.format.Sensor, optional
        A reference to the sensor, this value is represented in. Default is None.
    """

    uid: str
    name: str
    val: t.Union[int, float]
    sensor: Sensor = None

    @classmethod
    def fromdict(cls, data_dict: dict, sensors: dict) -> "Num":
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
            sensor=cls._coordinate_system_fromdict(data_dict, sensors),
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

        return {
            "uid": str(self.uid),
            "name": str(self.name),
            "val": self.val,
            "coordinate_system": str(self.sensor.uid),
        }

    @classmethod
    def _coordinate_system_fromdict(cls, data_dict: dict, sensors: dict) -> t.Optional[Sensor]:

        is_coordinate_system_in_data = (
            "coordinate_system" in data_dict and data_dict["coordinate_system"] != ""
        )

        if not is_coordinate_system_in_data:
            return None

        if data_dict["coordinate_system"] not in sensors:
            _warning(
                f"'{data_dict['coordinate_system']}' does not exist as a sensor, "
                + f"but is referenced for the annotation {data_dict['uid']}."
            )
            return None

        return sensors[data_dict["coordinate_system"]]
