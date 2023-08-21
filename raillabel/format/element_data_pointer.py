# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass
from enum import Enum

from ._annotation import _Annotation
from .frame_interval import FrameInterval
from .sensor import Sensor


@dataclass
class ElementDataPointer:
    """Container of pointers for annotations indexed by the "name" property.

    Used for indexing annotations for easy referencing without loading all of them.

    Parameters
    ----------
    sensor: raillabel.format.Sensor
        Sensor the referenced annotations are contained in.
    annotation_type: child class of raillabel.format._Annotation
        Class of the referenced annotations. Must be a child class of _Annotations.
    object: raillabel.format.Object
        Object the referenced annotations belong to.
    frame_intervals: list[raillabel.format.FrameInterval]
        Frame intervals, this element data pointer is contained in.
    attribute_pointers: dict[str, raillabel.format.element_data_pointers.AttributeType]
        References of attributes contained in the referenced annotations with attribute type.

    Properties (read-only)
    ----------------------
    uid: str
        Unique identifier of the ElementDataPointer built from the attributes.
    """

    sensor: Sensor
    annotation_type: t.Type[_Annotation]
    object: "raillabel.format.Object"
    frame_intervals: t.List[FrameInterval]
    attribute_pointers: t.Dict[str, "AttributeType"]

    @property
    def uid(self) -> str:
        """Return unique identifyer based on the properties."""
        return f"{self.sensor.uid}__{self.annotation_type.OPENLABEL_ID}__{self.object.type}"

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
            "type": self.annotation_type.OPENLABEL_ID,
            "frame_intervals": self._frame_intervals_asdict(),
            "attribute_pointers": self._attribute_pointers_asdict(),
        }

    def _frame_intervals_asdict(self) -> list[t.Dict[str, int]]:
        return [fi.asdict() for fi in self.frame_intervals]

    def _attribute_pointers_asdict(self) -> t.Dict[str, str]:
        return {
            attr_name: attr_type.value for attr_name, attr_type in self.attribute_pointers.items()
        }


class AttributeType(Enum):
    """Possible types of attributes."""

    BOOLEAN = "boolean"
    NUM = "num"
    TEXT = "text"
    VEC = "vec"
