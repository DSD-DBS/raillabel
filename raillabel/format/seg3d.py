# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing
from dataclasses import dataclass

from ._annotation import _Annotation


@dataclass
class Seg3d(_Annotation):
    """The 3D segmentation of a lidar pointcloud.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier of the annotation.
    name: str
        Human readable name describing the annotation.
    point_ids: list of int
        The list of point indices.
    attributes: dict, optional
        Attributes of the annotation. Default is {}.
    coordinate_system: raillabel.format.CoordinateSystem, optional
        The coordinate_system, this annotation is labeled in. Default is None.
    object_annotations: raillabel.format.ObjectAnnotations, optional
        ObjectAnnotations containing the Seg3d. Used for accessing higher level informations.
        Default is None.

    Parameters
    ----------
    uri: str
        URI to the file, which contains the annotated object.
    """

    point_ids: typing.List[int] = None

    _REQ_FIELDS = ["point_ids"]

    @classmethod
    def fromdict(
        self,
        data_dict: dict,
        coordinate_systems: dict,
        object_annotations=None,
    ) -> typing.Tuple["Seg3d", list]:
        """Generate a Bbox object from a dictionary in the OpenLABEL format.

        Parameters
        ----------
        data_dict: dict
            OpenLABEL format dictionary containing the data for the annotation.
        coordinate_systems: dict
            Dictionary containing all coordinate_systems for the scene.
        object_annotations: raillabel.format.ObjectAnnotations, optional
            ObjectAnnotations containing the Seg3d. Used for accessing higher level informations.
            Default is None.

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
        annotation = Seg3d(
            uid=str(data_dict["uid"]),
            name=str(data_dict["name"]),
            point_ids=data_dict["val"],
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

        dict_repr = self._annotation_required_fields_asdict()

        dict_repr["val"] = [int(pid) for pid in self.point_ids]

        dict_repr.update(self._annotation_optional_fields_asdict())

        return dict_repr

    def __eq__(self, __o: object) -> bool:
        """Compare this annotation with another one."""
        return super().equals(self, __o)
