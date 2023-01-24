# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing
from dataclasses import dataclass, field

from .coordinate_system import CoordinateSystem


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
    coordinate_system: raillabel.format.CoordinateSystem, optional
        A reference to the coordinate_system, this value is represented in. Default is None.
    """

    uid: str
    name: str
    val: typing.Union[int, float]
    attributes: typing.Dict[
        str, typing.Union[int, float, bool, str, list]
    ] = field(default_factory=dict)
    coordinate_system: CoordinateSystem = None

    @classmethod
    def fromdict(
        self, data_dict: dict, coordinate_systems: dict
    ) -> typing.Tuple[dict, list]:
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

        warnings = (
            []
        )  # list of warnings, that have occurred during the parsing

        # Creates the annotation with all mandatory properties
        annotation = Num(
            uid=str(data_dict["uid"]),
            name=str(data_dict["name"]),
            val=data_dict["val"],
        )

        # Adds the optional properties
        if (
            "coordinate_system" in data_dict
            and data_dict["coordinate_system"] != ""
        ):
            try:
                annotation.coordinate_system = coordinate_systems[
                    data_dict["coordinate_system"]
                ]

            except KeyError:
                warnings.append(
                    f"{data_dict['coordinate_system']} does not exist as a coordinate system, "
                    + f"but is referenced for the annotation {data_dict['uid']}."
                )

        # Adds the attributes
        if "attributes" in data_dict:

            annotation.attributes = d = {
                a["name"]: a["val"]
                for l in data_dict["attributes"].values()
                for a in l
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

        dict_repr = {
            "uid": str(self.uid),
            "name": str(self.name),
            "val": float(self.val) if type(self.val) != int else self.val,
        }

        if self.coordinate_system != None:
            dict_repr["coordinate_system"] = str(self.coordinate_system.uid)

        if self.attributes != {}:
            dict_repr["attributes"] = {}

            for attr_name, attr_value in self.attributes.items():

                # Since the annotation stores the attributes in a collective
                # dictionary, they must be seperated by type in order to comply
                # with the OpenLabel format.

                if type(attr_value) == str:
                    attr_type = "text"

                elif type(attr_value) in [float, int]:
                    attr_type = "num"

                elif type(attr_value) == bool:
                    attr_type = "boolean"

                elif type(attr_value) in [list, tuple]:
                    attr_type = "vec"

                else:
                    raise TypeError(
                        f"Attribute type {type(attr_value)} of {attr_value} is not supported. "
                        + "Supported types are str, float, int, bool, list, tuple."
                    )

                if attr_type not in dict_repr["attributes"]:
                    dict_repr["attributes"][attr_type] = []

                dict_repr["attributes"][attr_type].append(
                    {"name": attr_name, "val": attr_value}
                )

        return dict_repr
