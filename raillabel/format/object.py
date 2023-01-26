# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing
from dataclasses import dataclass, field

from .coordinate_system import CoordinateSystem
from .frame_interval import FrameInterval


@dataclass
class Object:
    """Physical, unique object in the data, that can be tracked via its UID.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier for the object.
    name: str
        Name of the object. It is a friendly name and not used for indexing. Commonly the class
        name is used followed by an underscore and an integer (i.e. person_0032).
    type: str
        The type of an object defines the class the object corresponds to.
    coordinate_system: raillabel.format.CoordinateSystem, optional
        This is the coordinate system this object is referenced in. Default is None.
    frame_intervals: list of raillabel.format.FrameInterval, optional
        The array of frame intervals where this action exists or is defined. Default is [].
    """

    uid: str
    name: str
    type: str
    coordinate_system: CoordinateSystem = None
    frame_intervals: typing.List[FrameInterval] = field(default_factory=list)

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

        dict_repr = {"name": str(self.name), "type": str(self.type)}

        if self.coordinate_system is not None:
            dict_repr["coordinate_system"] = str(self.coordinate_system.uid)

        if self.frame_intervals != []:
            dict_repr["frame_intervals"] = [fi.asdict() for fi in self.frame_intervals]

        return dict_repr
