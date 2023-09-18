# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
import uuid
from dataclasses import dataclass
from decimal import Decimal

from ..._util._warning import _warning
from ._annotation import _Annotation
from ._translation import translate_class_id, translate_sensor_id
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
        Dictionary containing all annotations. The keys are the uids of the annotations and the
        values are objects of type BoundingBox2d, BoundingBox3d, Polygon2d, Polyline2d or
        Segementation3d.
    """

    id: int
    timestamp: Decimal
    bounding_box_2ds: t.Dict[str, BoundingBox2d]
    bounding_box_3ds: t.Dict[str, BoundingBox3d]
    polygon_2ds: t.Dict[str, Polygon2d]
    polyline_2ds: t.Dict[str, Polyline2d]
    segmentation_3ds: t.Dict[str, Segmentation3d]

    _annotation_uids: t.Set[str] = None

    @property
    def annotations(self) -> dict:
        """Return all annotations of this frame in one dict."""
        return {
            **self.bounding_box_2ds,
            **self.polyline_2ds,
            **self.polygon_2ds,
            **self.bounding_box_3ds,
            **self.segmentation_3ds,
        }

    @property
    def translated_objects(self) -> dict:
        """Return all objects in this frame and translate them.

        Returns
        -------
        dict
            Dictionary containing all objects. Keys are the object IDs and values are the
            translated class names.
        """
        return {
            str(a.object_id): translate_class_id(a.class_name) for a in self.annotations.values()
        }

    @property
    def translated_sensors(self) -> dict:
        """Return all sensors in this frame and translates them.

        Returns
        -------
        dict
            Dictionary containing all sensors. Keys are the translated sensor IDs and values are
            the SensorReference objects.
        """
        sensors_list = []

        for annotation in list(self.annotations.values()):
            sensors_list.append(annotation.sensor)
            sensors_list[-1].type = translate_sensor_id(sensors_list[-1].type)

        return {sensor.type: sensor for sensor in sensors_list}

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

        cls._annotation_uids = set()

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

    def to_raillabel(self) -> dict:
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
        return {
            "frame_properties": self._frame_properties_to_raillabel(),
            "objects": self._objects_to_raillabel(),
        }

    @classmethod
    def _annotation_fromdict(
        cls, data_dict: dict, annotation_class: t.Type[_Annotation]
    ) -> t.Dict[str, t.Type[_Annotation]]:

        annotations = {}
        for annotation_dict in data_dict:
            annotation_dict["id"] = cls._check_duplicate_annotation_uid(annotation_dict["id"])
            annotations[annotation_dict["id"]] = annotation_class.fromdict(annotation_dict)

        return {ann["id"]: annotation_class.fromdict(ann) for ann in data_dict}

    @classmethod
    def _check_duplicate_annotation_uid(cls, uid: str) -> str:

        if uid in cls._annotation_uids:
            _warning(
                f"Annotation uid {uid} is contained more than once. A new uid will be assigned."
            )
            return str(uuid.uuid4())

        cls._annotation_uids.add(uid)
        return uid

    def _frame_properties_to_raillabel(self) -> dict:

        streams_dict = {}
        for stream_id, stream in self.translated_sensors.items():
            streams_dict[stream_id] = {
                "stream_properties": {"sync": {"timestamp": str(stream.timestamp)}},
                "uri": stream.uri.split("/")[-1],
            }

        return {
            "timestamp": str(self.timestamp),
            "streams": {
                sensor.type: sensor.to_raillabel()[1] for sensor in self.translated_sensors.values()
            },
        }

    def _objects_to_raillabel(self) -> dict:
        object_data = {}

        for annotation in self.annotations.values():

            object_id = str(annotation.object_id)

            if object_id not in object_data:
                object_data[object_id] = {"object_data": {}}

            if annotation.OPENLABEL_ID not in object_data[object_id]["object_data"]:
                object_data[object_id]["object_data"][annotation.OPENLABEL_ID] = []

            object_data[object_id]["object_data"][annotation.OPENLABEL_ID].append(
                annotation.to_raillabel()[0]
            )

        return object_data
