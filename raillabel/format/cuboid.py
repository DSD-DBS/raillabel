# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing
from dataclasses import dataclass, field

from .coordinate_system import CoordinateSystem
from .point3d import Point3d
from .quaternion import Quaternion
from .size3d import Size3d


@dataclass
class Cuboid:
    """3D bounding box.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier of the annotation.
    name: str
        Human readable name describing the annotation.
    pos: raillabel.format.Point3d
        The center position of the cuboid in meters, where the x coordinate points ahead of the
        vehicle, y points to the left and z points upwards.
    quat: raillabel.format.Quaternion
        The rotation of the cuboid in quaternions.
    size: raillabel.format.Size3d
        The size of the cuboid in meters.
    attributes: dict, optional
        Attributes of the annotation. Dict keys are the name str of the attribute, values are the
        attribute values. Default is {}.
    coordinate_system: raillabel.format.CoordinateSystem, optional
        A reference to the coordinate_system, this annotation is labeled in. Default is None.
    object_annotations: raillabel.format.ObjectAnnotations, optional
        ObjectAnnotations containing the Cuboid. Used for accessing higher level informations.
        Default is None.

    Parameters
    ----------
    uri: str
        URI to the file, which contains the annotated object.
    """

    uid: str
    name: str
    pos: Point3d
    quat: Quaternion
    size: Size3d
    attributes: typing.Dict[
        str, typing.Union[int, float, bool, str, list]
    ] = field(default_factory=dict)
    coordinate_system: CoordinateSystem = None
    object_annotations: typing.Any = None

    @property
    def uri(self) -> str or None:
        """URI to the file, which contains the annotated object."""
        if (
            self.object_annotations == None
            or self.object_annotations.frame == None
        ):
            return None
        return self.object_annotations.frame.streams[
            self.coordinate_system.uid
        ].uri

    @uri.setter
    def uri(self, value):

        if self.object_annotations == None:
            raise AttributeError(
                f"Attribute object_annotations not set for annotation {self.uri}."
            )

        if self.object_annotations.frame == None:
            raise AttributeError(
                f"Attribute frame not set for ObjectAnnotation of annotation {self.uri}."
            )

        self.object_annotations.frame.streams[
            self.coordinate_system.uid
        ].uri = value

    @classmethod
    def fromdict(
        self,
        data_dict: dict,
        coordinate_systems: dict,
        object_annotations=None,
    ) -> typing.Tuple["Cuboid", list]:
        """Generate a Cuboid object from a dictionary in the OpenLABEL format.

        Parameters
        ----------
        data_dict: dict
            OpenLABEL format dictionary containing the data for the annotation.
        coordinate_systems: dict
            Dictionary containing all coordinate_systems for the scene.
        object_annotations: raillabel.format.ObjectAnnotations, optional
            ObjectAnnotations containing the Cuboid. Used for accessing higher level informations.
            Default is None.

        Returns
        -------
        annotation: Cuboid
            Converted annotation.
        warnings: list of str
            List of non-critical errors, that have occurred during the conversion.
        """

        warnings = (
            []
        )  # list of warnings, that have occurred during the parsing

        # Creates the annotation with all mandatory properties
        annotation = Cuboid(
            uid=str(data_dict["uid"]),
            name=str(data_dict["name"]),
            pos=Point3d(
                x=data_dict["val"][0],
                y=data_dict["val"][1],
                z=data_dict["val"][2],
            ),
            quat=Quaternion(
                x=data_dict["val"][3],
                y=data_dict["val"][4],
                z=data_dict["val"][5],
                w=data_dict["val"][6],
            ),
            size=Size3d(
                x=data_dict["val"][7],
                y=data_dict["val"][8],
                z=data_dict["val"][9],
            ),
            object_annotations=object_annotations,
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
            "val": [
                float(self.pos.x),
                float(self.pos.y),
                float(self.pos.z),
                float(self.quat.x),
                float(self.quat.y),
                float(self.quat.z),
                float(self.quat.w),
                float(self.size.x),
                float(self.size.y),
                float(self.size.z),
            ],
        }

        if self.coordinate_system != None:
            dict_repr["coordinate_system"] = str(self.coordinate_system.uid)

        if self.attributes != {} or self.uri != None:
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

    def __eq__(self, __o: object) -> bool:
        """Compare this annotation with another one."""

        if type(__o) != type(self):
            return False

        # object_annotations is omitted from the equal comparison, because it contains this
        # annotation, which will lead to a RecursionError.
        return {
            k: v for k, v in vars(self).items() if k != "object_annotations"
        } == {k: v for k, v in vars(__o).items() if k != "object_annotations"}
