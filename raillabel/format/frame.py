# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import decimal
import typing as t
from dataclasses import dataclass, field

from ._object_annotation import _ObjectAnnotation, annotation_classes
from .num import Num
from .object import Object
from .sensor import Sensor
from .sensor_reference import SensorReference


@dataclass
class Frame:
    """A container of dynamic, timewise, information.

    Parameters
    ----------
    timestamp: decimal.Decimal, optional
        Timestamp containing the Unix epoch time of the frame with up to nanosecond precision.
    sensors: dict of raillabel.format.SensorReference, optional
        References to the sensors with frame specific information like timestamp and uri.
        Default is {}.
    frame_data: dict, optional
        Dictionary containing data directly connected to the frame and not to any object, like
        gps/imu data. Dictionary keys are the ID-strings of the variable the data belongs to.
        Default is {}.
    annotations: dict[str, _ObjectAnnotation subclass], optional
        Dictionary containing all annotations of this frame. Keys are annotation uids.

    Read-Only Attributes
    --------------------
    object_data: dict[str, dict[str, _ObjectAnnotation subclass]]
        Annotations categorized by object. Keys are object uids and values are the annotations
        as a dict, that are part of the object.

    """

    timestamp: decimal.Decimal | None = None
    sensors: dict[str, SensorReference] = field(default_factory=dict)
    frame_data: dict[str, Num] = field(default_factory=dict)
    annotations: dict[str, type[_ObjectAnnotation]] = field(default_factory=dict)

    @property
    def object_data(self) -> dict[str, dict[str, type[_ObjectAnnotation]]]:
        """Return annotations categorized by Object-Id.

        Returns
        -------
        dict[str, dict[UUID, _ObjectAnnotation subclass]]
            Dictionary of annotations. Keys are object uids and values are annotations, that are
            contained in the object.

        """
        object_data: dict[str, dict[str, type[_ObjectAnnotation]]] = {}
        for ann_id, annotation in self.annotations.items():
            if annotation.object.uid not in object_data:
                object_data[annotation.object.uid] = {}

            object_data[annotation.object.uid][ann_id] = annotation

        return object_data

    @classmethod
    def fromdict(
        cls,
        data_dict: dict,
        objects: dict[str, Object],
        sensors: dict[str, Sensor],
    ) -> Frame:
        """Generate a Frame object from a dict.

        Parameters
        ----------
        uid: str
            Unique identifier of the frame.
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        objects: dict
            Dictionary of all objects in the scene.
        sensors: dict
            Dictionary of all sensors in the scene.

        Returns
        -------
        frame: raillabel.format.Frame
            Converted Frame object.

        """
        return Frame(
            timestamp=cls._timestamp_fromdict(data_dict),
            sensors=cls._sensors_fromdict(data_dict, sensors),
            frame_data=cls._frame_data_fromdict(data_dict, sensors),
            annotations=cls._objects_fromdict(data_dict, objects, sensors),
        )

    def asdict(self) -> dict[str, t.Any]:
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
        dict_repr: dict[str, t.Any] = {}

        if self.timestamp is not None or self.sensors != {} or self.frame_data != {}:
            dict_repr["frame_properties"] = {}

        if self.timestamp is not None:
            dict_repr["frame_properties"]["timestamp"] = str(self.timestamp)

        if self.sensors != {}:
            dict_repr["frame_properties"]["streams"] = {
                str(k): v.asdict() for k, v in self.sensors.items()
            }

        if self.frame_data != {}:
            dict_repr["frame_properties"]["frame_data"] = {
                "num": [v.asdict() for v in self.frame_data.values()]
            }

        if self.annotations != {}:
            dict_repr["objects"] = self._annotations_asdict()

        return dict_repr

    @classmethod
    def _timestamp_fromdict(cls, data_dict: dict) -> decimal.Decimal | None:
        if "frame_properties" not in data_dict or "timestamp" not in data_dict["frame_properties"]:
            return None

        return decimal.Decimal(data_dict["frame_properties"]["timestamp"])

    @classmethod
    def _sensors_fromdict(
        cls, data_dict: dict, scene_sensors: dict[str, Sensor]
    ) -> dict[str, SensorReference]:
        if "frame_properties" not in data_dict or "streams" not in data_dict["frame_properties"]:
            return {}

        sensors = {}

        for sensor_id, sensor_dict in data_dict["frame_properties"]["streams"].items():
            sensors[sensor_id] = SensorReference.fromdict(
                data_dict=sensor_dict, sensor=scene_sensors[sensor_id]
            )

        return sensors

    @classmethod
    def _frame_data_fromdict(cls, data_dict: dict, sensors: dict[str, Sensor]) -> dict[str, Num]:
        if "frame_properties" not in data_dict or "frame_data" not in data_dict["frame_properties"]:
            return {}

        frame_data = {}
        for ann_type in data_dict["frame_properties"]["frame_data"]:
            for ann_raw in data_dict["frame_properties"]["frame_data"][ann_type]:
                frame_data[ann_raw["name"]] = Num.fromdict(ann_raw, sensors)

        return frame_data

    @classmethod
    def _objects_fromdict(
        cls,
        data_dict: dict,
        objects: dict[str, Object],
        sensors: dict[str, Sensor],
    ) -> dict[str, type[_ObjectAnnotation]]:
        if "objects" not in data_dict:
            return {}

        annotations = {}

        for obj_id, obj_ann in data_dict["objects"].items():
            object_annotations = cls._object_annotations_fromdict(
                data_dict=obj_ann["object_data"],
                object=objects[obj_id],
                sensors=sensors,
            )

            for annotation in object_annotations:
                annotations[annotation.uid] = annotation

        return annotations

    @classmethod
    def _object_annotations_fromdict(
        cls,
        data_dict: dict,
        object: Object,
        sensors: dict[str, Sensor],
    ) -> t.Iterator[type[_ObjectAnnotation]]:
        for ann_type, annotations_raw in data_dict.items():
            for ann_raw in annotations_raw:
                yield annotation_classes()[ann_type].fromdict(ann_raw, sensors, object)

    def _annotations_asdict(self) -> dict[str, t.Any]:
        annotations_dict: dict[str, t.Any] = {}
        for object_id, annotations_ in self.object_data.items():
            annotations_dict[object_id] = {"object_data": {}}

            for annotation in annotations_.values():
                if annotation.OPENLABEL_ID not in annotations_dict[object_id]["object_data"]:
                    annotations_dict[object_id]["object_data"][annotation.OPENLABEL_ID] = []

                annotations_dict[object_id]["object_data"][annotation.OPENLABEL_ID].append(
                    annotation.asdict()  # type: ignore
                )

        return annotations_dict
