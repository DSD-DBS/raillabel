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
    coordinate_system: raillabel.format.CoordinateSystem, optional
        A reference to the coordinate_system, this value is represented in. Default is None.
    """

    val: t.Union[int, float] = None

    OBJECT_DATA_FIELD = "nums"
    _REQ_FIELDS = ["val"]

    @classmethod
    def fromdict(self, data_dict: dict, coordinate_systems: dict) -> t.Tuple[dict, list]:
        """Generate a Bbox object from a dictionary in the OpenLABEL format.

        Parameters
        ----------
        data_dict: dict
            OpenLABEL format dictionary containing the data for the annotation.
        coordinate_systems: dict
            Dictionary containing all coordinate_systems for the scene.

        Returns
        -------
        annotation: Bbox
            Converted annotation.
        warnings: list of str
            List of non-critical errors, that have occurred during the conversion.
        """

        warnings = []  # list of warnings, that have occurred during the parsing

        # Creates the annotation with all mandatory properties
        annotation = Num(
            uid=str(data_dict["uid"]),
            name=str(data_dict["name"]),
            val=data_dict["val"],
        )

        # Adds the optional properties
        if "coordinate_system" in data_dict and data_dict["coordinate_system"] != "":
            try:
                annotation.coordinate_system = coordinate_systems[data_dict["coordinate_system"]]

            except KeyError:
                warnings.append(
                    f"{data_dict['coordinate_system']} does not exist as a coordinate system, "
                    + f"but is referenced for the annotation {data_dict['uid']}."
                )

        # Adds the attributes
        if "attributes" in data_dict:

            annotation.attributes = {
                a["name"]: a["val"] for l in data_dict["attributes"].values() for a in l
            }

            # Saves the uri attribute as a class attribute
            if "uri" in annotation.attributes:
                annotation.uri = annotation.attributes["uri"]
                del annotation.attributes["uri"]

        return annotation, warnings

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

    def __eq__(self, __o: object) -> bool:
        """Compare this annotation with another one."""
        return super().equals(self, __o)
