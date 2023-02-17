# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass

from ._annotation import _Annotation
from .point2d import Point2d


@dataclass
class Poly2d(_Annotation):
    """Sequence of 2D points. Can either be a polygon or polyline.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier for the annotation.
    name: str
        Human readable name describing the annotation.
    points: list of raillabel.format.Point2d
        List of the 2d points that make up the polyline.
    closed: bool
        This parameter states, whether the polyline represents a closed shape (a polygon) or an
        open line.
    mode: str, optional
        Mode of the polyline list of values: "MODE_POLY2D_ABSOLUTE" determines that the poly2d list
        contains the sequence of (x, y) values of all points of the polyline. "MODE_POLY2D_RELATIVE"
        specifies that only the first point of the sequence is defined with its (x, y) values, while
        all the rest are defined relative to it. "MODE_POLY2D_SRF6DCC" specifies that SRF6DCC chain
        code method is used. "MODE_POLY2D_RS6FCC" specifies that the RS6FCC method is used. Default
        is 'MODE_POLY2D_ABSOLUTE'.
    attributes: dict, optional
        Attributes of the annotation. Dict keys are the name str of the attribute, values are the
        attribute values. Default is {}.
    sensor: raillabel.format.CoordinateSystem, optional
        A reference to the sensor, this annotation is labeled in. Default is None.
    """

    points: t.List[Point2d] = None
    closed: bool = None
    mode: str = "MODE_POLY2D_ABSOLUTE"

    _REQ_FIELDS = ["points", "closed"]

    @classmethod
    def fromdict(
        self,
        data_dict: dict,
        sensors: dict,
    ) -> t.Tuple["Poly2d", list]:
        """Generate a Bbox object from a dictionary in the OpenLABEL format.

        Parameters
        ----------
        data_dict: dict
            OpenLABEL format dictionary containing the data for the annotation.
        sensors: dict
            Dictionary containing all sensors for the scene.

        Returns
        -------
        annotation: Bbox
            Converted annotation.
        warnings: list of str
            List of non-critical errors, that have occurred during the conversion.
        """

        warnings = []  # list of warnings, that have occurred during the parsing

        # Parses the points
        points = []
        for i in range(0, len(data_dict["val"]), 2):
            points.append(Point2d(x=data_dict["val"][i], y=data_dict["val"][i + 1]))

        # Creates the annotation with all mandatory properties
        annotation = Poly2d(
            uid=str(data_dict["uid"]),
            name=str(data_dict["name"]),
            closed=data_dict["closed"],
            mode=data_dict["mode"],
            points=points,
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

        dict_repr["closed"] = bool(self.closed)
        dict_repr["val"] = []
        dict_repr["mode"] = self.mode
        for point in self.points:
            dict_repr["val"].extend(point.asdict())

        dict_repr.update(self._annotation_optional_fields_asdict())

        return dict_repr
