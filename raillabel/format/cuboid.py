# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from ._annotation import _Annotation
from .point3d import Point3d
from .quaternion import Quaternion
from .size3d import Size3d


@dataclass
class Cuboid(_Annotation):
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
    sensor: raillabel.format.CoordinateSystem, optional
        A reference to the sensor, this annotation is labeled in. Default is None.
    """

    pos: Point3d = None
    quat: Quaternion = None
    size: Size3d = None

    _REQ_FIELDS = ["pos", "size", "quat"]

    @classmethod
    def fromdict(
        self,
        data_dict: dict,
        sensors: dict,
    ) -> t.Tuple["Cuboid", list]:
        """Generate a Cuboid object from a dictionary in the OpenLABEL format.

        Parameters
        ----------
        data_dict: dict
            OpenLABEL format dictionary containing the data for the annotation.
        sensors: dict
            Dictionary containing all sensors for the scene.

        Returns
        -------
        annotation: Cuboid
            Converted annotation.
        warnings: list of str
            List of non-critical errors, that have occurred during the conversion.
        """

        warnings = []  # list of warnings, that have occurred during the parsing

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
        )

        # Adds the optional properties
        if "coordinate_system" in data_dict and data_dict["coordinate_system"] != "":
            try:
                annotation.sensor = sensors[data_dict["coordinate_system"]]

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

        dict_repr["val"] = [
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
        ]

        dict_repr.update(self._annotation_optional_fields_asdict())

        return dict_repr
