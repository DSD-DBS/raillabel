# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass
from decimal import Decimal

from ._annotation import _Annotation
from ._translation import translate_sensor_id
from .bounding_box_2d import BoundingBox2d
from .bounding_box_3d import BoundingBox3d
from .polygon_2d import Polygon2d
from .polyline_2d import Polyline2d
from .segmentation_3d import Segmentation3d


@dataclass
class Frame:
    """A container of dynamic, timewise, information.

    Parameters
    ----------
    id: int
        Numerical identifier of the frame. Must be unique within the scene.
    timestamp: decimal.Decimal
        Timestamp containing the Unix epoch time of the frame with up to nanosecond precision.
    annotations: dict
        Dictionary containing all annotations. The keys are the uids of the annotations and the values are objects of type BoundingBox2d, BoundingBox3d, Polygon2d, Polyline2d or Segementation3d.
    """

    id: int
    timestamp: Decimal
    bounding_box_2ds: t.Dict[str, BoundingBox2d]
    bounding_box_3ds: t.Dict[str, BoundingBox3d]
    polygon_2ds: t.Dict[str, Polygon2d]
    polyline_2ds: t.Dict[str, Polyline2d]
    segmentation_3ds: t.Dict[str, Segmentation3d]

    @classmethod
    def fromdict(cls, data_dict: dict) -> "Frame":
        """Generate a Frame from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        Frame
            Converted frame.
        """

        return Frame(
            id=int(data_dict["frameId"]),
            timestamp=Decimal(data_dict["timestamp"]),
            bounding_box_2ds=cls._annotation_fromdict(
                data_dict["annotations"]["2D_BOUNDING_BOX"], BoundingBox2d
            ),
            bounding_box_3ds=cls._annotation_fromdict(
                data_dict["annotations"]["3D_BOUNDING_BOX"], BoundingBox3d
            ),
            polygon_2ds=cls._annotation_fromdict(data_dict["annotations"]["2D_POLYGON"], Polygon2d),
            polyline_2ds=cls._annotation_fromdict(
                data_dict["annotations"]["2D_POLYLINE"], Polyline2d
            ),
            segmentation_3ds=cls._annotation_fromdict(
                data_dict["annotations"]["3D_SEGMENTATION"], Segmentation3d
            ),
        )

    def to_raillabel(self) -> t.Tuple[dict, t.List[str], t.Dict[str, str]]:
        """Generate a Frame from a dictionary in the UAI format.

        Parameters
        ----------
        data_dict: dict
            Understand.AI T4 format dictionary containing the data_dict.

        Returns
        -------
        Frame
            Converted frame.
        list[str]
            List of sensor ids contained in the frame.
        dict[str, str]
            Dictionary with one item per object in the frame. Keys are the object UUIDs, the
            values are the class names.
        """
        return (
            {
                "frame_properties": self._frame_properties_to_raillabel(),
                "objects": self._objects_to_raillabel(),
            },
            list(self._contained_sensors().keys()),
            list(self._contained_objects().keys()),
        )

    @classmethod
    def _annotation_fromdict(
        cls, data_dict: dict, annotation_class: t.Type[_Annotation]
    ) -> t.Dict[str, BoundingBox2d]:
        return {ann["id"]: annotation_class.fromdict(ann) for ann in data_dict}
