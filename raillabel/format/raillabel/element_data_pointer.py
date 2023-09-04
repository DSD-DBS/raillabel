# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from ..._util._attribute_type import AttributeType
from .frame_interval import FrameInterval


@dataclass
class ElementDataPointer:
    """Container of pointers for annotations indexed by the "name" property.

    Used for indexing annotations for easy referencing without loading all of them.

    Parameters
    ----------
    uid: str
        Unique identifier of the ElementDataPointer assembled using a specific schema.
    frame_intervals: list[raillabel.format.FrameInterval]
        Frame intervals, this element data pointer is contained in.
    attribute_pointers: dict[str, raillabel.util._attribute_type.AttributeType]
        References of attributes contained in the referenced annotations with attribute type.

    Properties (read-only)
    ----------------------
    uid: str
        Unique identifier of the ElementDataPointer built from the attributes.
    """

    uid: str
    frame_intervals: t.List[FrameInterval]
    attribute_pointers: t.Dict[str, AttributeType]

    @property
    def annotation_type(self) -> str:
        """Return type of annotation e.g. bbox, cuboid."""
        return self.uid.split("__")[1]

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
            "type": self.annotation_type,
            "frame_intervals": self._frame_intervals_asdict(),
            "attribute_pointers": self._attribute_pointers_asdict(),
        }

    def _frame_intervals_asdict(self) -> t.List[t.Dict[str, int]]:
        return [fi.asdict() for fi in self.frame_intervals]

    def _attribute_pointers_asdict(self) -> t.Dict[str, str]:
        return {
            attr_name: attr_type.value for attr_name, attr_type in self.attribute_pointers.items()
        }
