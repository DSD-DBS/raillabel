# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing
from dataclasses import dataclass, field

from .transform import Transform


@dataclass
class CoordinateSystem:
    """Spatial 3D reference frame.

    Coordinate systems contain a rotational and translational transformation to a parent coordinate
    system (usually the base on the front-middle of the vehicle).

    Parameters
    ----------
    uid: str
        This is the friendly name of the coordinate_system as well as its identifier. Must be
        unique.
    type: str
        This is a string that describes the type of the coordinate system, for example, "local",
        "sensor", "geo".
    parent: raillabel.format.CoordinateSystem, optional
        A reference to the parent coordinate system, this CoordinateSystem is based on. If this
        this coordinate system has no parent (i.e. the base coordinate system), the parent should
        be None. Default is None.
    children: dict of raillabel.format.CoordinateSystem, optional
        Dictionary of children of this coordinate system. Dict keys are the uid strings of the
        child coordinate system. Dict values are references to those children. Default is {}.
    transform: raillabel.format.Transform, optional
        A transformation between this coordinate systems and its parent. Default is None.
    """

    uid: str
    type: str
    parent: "CoordinateSystem" = None
    children: typing.Dict[str, "CoordinateSystem"] = field(default_factory=dict)
    transform: Transform = None

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

        dict_repr = {"type": str(self.type)}

        if self.parent is not None:
            dict_repr["parent"] = self.parent.uid
        else:
            dict_repr["parent"] = ""

        if self.children != []:
            dict_repr["children"] = [c.uid for c in self.children.values()]

        if self.transform is not None:
            dict_repr["pose_wrt_parent"] = self.transform.asdict()

        return dict_repr

    def __eq__(self, other) -> bool:
        """Handels equal comparisons."""

        # Because this class contains attribute, that have in turn the class itself as its type
        # (self.parent, self.children), not implementing a custom __eq__() would raise a
        # RecursionError.

        if not hasattr(other, "__dict__"):
            return False

        if len(self.__dict__) != len(other.__dict__):
            return False

        for attr in self.__dict__:

            if type(getattr(self, attr)) == type(self):
                if getattr(self, attr).uid != getattr(other, attr).uid:
                    return False

            elif type(getattr(self, attr)) in [dict, list, tuple]:
                for key in getattr(self, attr).keys():
                    if type(getattr(self, attr)[key]) == type(self):

                        try:
                            if getattr(self, attr)[key].uid != getattr(other, attr)[key].uid:
                                return False
                        except KeyError:
                            return False

                    else:
                        try:
                            if getattr(self, attr)[key].uid != getattr(other, attr)[key].uid:
                                return False
                        except KeyError:
                            return False

            else:
                if getattr(self, attr) != getattr(other, attr):
                    return False

        return True
