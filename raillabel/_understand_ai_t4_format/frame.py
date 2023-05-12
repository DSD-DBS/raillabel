# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

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
    annotations: t.Dict[
        str, t.Union[BoundingBox2d, BoundingBox3d, Polygon2d, Polyline2d, Segmentation3d]
    ]

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
            annotations=cls._annotations_fromdict(data_dict["annotations"]),
        )

    @classmethod
    def _annotations_fromdict(
        cls, data_dict: dict
    ) -> t.Dict[str, t.Union[BoundingBox2d, BoundingBox3d, Polygon2d, Polyline2d, Segmentation3d]]:
        annotations = {}

        for ann in data_dict["2D_BOUNDING_BOX"]:
            annotations[ann["id"]] = BoundingBox2d.fromdict(ann)

        for ann in data_dict["3D_BOUNDING_BOX"]:
            annotations[ann["id"]] = BoundingBox3d.fromdict(ann)

        for ann in data_dict["2D_POLYGON"]:
            annotations[ann["id"]] = Polygon2d.fromdict(ann)

        for ann in data_dict["2D_POLYLINE"]:
            annotations[ann["id"]] = Polyline2d.fromdict(ann)

        for ann in data_dict["3D_SEGMENTATION"]:
            annotations[ann["id"]] = Segmentation3d.fromdict(ann)

        return annotations
