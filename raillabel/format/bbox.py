# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass

from ._annotation import _Annotation
from .point2d import Point2d
from .size2d import Size2d


@dataclass
class Bbox(_Annotation):
    """A 2D bounding box in an image.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier of the annotation.
    name: str
        Human readable name describing the annotation.
    pos: raillabel.format.Point2d
        The center point of the bbox in pixels.
    size: raillabel.format.Size2d
        The dimensions of the bbox in pixels from the top left corner to the bottom right corner.
    attributes: dict, optional
        Attributes of the annotation. Dict keys are the name str of the attribute, values are the
        attribute values. Default is {}.
    sensor: raillabel.format.CoordinateSystem, optional
        A reference to the sensor, this annotation is labeled in. Default is None.
    """

    pos: Point2d = None
    size: Size2d = None

    OPENLABEL_ID = "bbox"
    _REQ_FIELDS = ["pos", "size"]

    @classmethod
    def fromdict(self, data_dict: dict, sensors: dict) -> "Bbox":
        """Generate a Bbox object from a dict.

        Parameters
        ----------
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        sensors: dict
            Dictionary containing all sensors for the scene.

        Returns
        -------
        annotation: Bbox
            Converted annotation.
        """

        return Bbox(
            uid=str(data_dict["uid"]),
            name=str(data_dict["name"]),
            pos=Point2d(x=data_dict["val"][0], y=data_dict["val"][1]),
            size=Size2d(x=data_dict["val"][2], y=data_dict["val"][3]),
            sensor=self._coordinate_system_fromdict(data_dict, sensors),
            attributes=self._attributes_fromdict(data_dict),
        )

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
            float(self.size.x),
            float(self.size.y),
        ]

        dict_repr.update(self._annotation_optional_fields_asdict())

        return dict_repr
