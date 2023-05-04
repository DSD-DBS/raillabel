# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import decimal
import logging
import typing as t
import uuid
from dataclasses import dataclass, field

from .num import Num
from .object import Object
from .object_data import ObjectData
from .sensor import Sensor
from .sensor_reference import SensorReference


@dataclass
class Frame:
    """A container of dynamic, timewise, information.

    Parameters
    ----------
    uid: int
        Number of the frame withing the annotation file. Must be unique.
    timestamp: decimal.Decimal, optional
        Timestamp containing the Unix epoch time of the frame with up to nanosecond precision.
    sensors: dict of raillabel.format.SensorReference, optional
        References to the sensors with frame specific information like timestamp and uri.
        Default is {}.
    data: dict, optional
        Dictionary containing data directly connected to the frame and not to anny object.
        Dictionary keys are the ID-strings of the variable the data belongs to. Default is {}.
    object_data: dict of raillabel.format.ObjectData, optional
        Dictionary containing the annotations per object. Dictionary keys are the object uids.
        Default is {}.

    Read-Only Attributes
    --------------------
    annotations: dict
        Dictionary containing all annotations of this frame, regardless of object or annotation
        type. Dictionary keys are annotation UIDs.
    """

    uid: int
    timestamp: t.Optional[decimal.Decimal] = None
    sensors: t.Dict[str, SensorReference] = field(default_factory=dict)
    data: t.Dict[str, Num] = field(default_factory=dict)
    object_data: t.Dict[uuid.UUID, ObjectData] = field(default_factory=dict)

    @property
    def annotations(self) -> t.Dict[uuid.UUID, t.Any]:
        """Return dict containing all annotations of this frame.

        Dictionary keys are annotation UIDs.
        """
        annotations = {}
        for object in self.object_data.values():
            annotations.update(object.annotations)

        return annotations

    @classmethod
    def fromdict(
        cls,
        uid: str,
        data_dict: dict,
        objects: t.Dict[str, Object],
        sensors: t.Dict[str, Sensor],
        annotation_classes: dict,
    ) -> "Frame":
        """Generate a Frame object from a dictionary in the RailLabel format.

        Parameters
        ----------
        uid: str
            Unique identifier of the frame.
        data_dict: dict
            Dict representation of the frame.
        objects: dict
            Dictionary of all objects in the scene.
        sensors: dict
            Dictionary of all sensors in the scene.
        annotation_classes: dict
            Dictionary conaining all of the annotation classes as values with the OpenLABEL identifiers as keys.

        Returns
        -------
        frame: raillabel.format.Frame
            Converted Frame object.
        """

        data_dict = cls._prepare_data(data_dict)

        frame = Frame(
            uid=int(uid),
            timestamp=cls._timestamp_fromdict(data_dict),
            sensors=cls._sensors_fromdict(data_dict, int(uid), sensors),
            data=cls._frame_data_fromdict(data_dict, int(uid), annotation_classes, sensors),
            object_data=cls._objects_fromdict(
                data_dict, int(uid), objects, sensors, annotation_classes
            ),
        )

        frame = cls._fix_sensor_uri_attribute(frame)

        return frame

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

        dict_repr = {}

        if self.timestamp is not None or self.sensors != {}:
            dict_repr["frame_properties"] = {}

        if self.timestamp is not None:
            dict_repr["frame_properties"]["timestamp"] = str(self.timestamp)

        if self.sensors != {}:
            dict_repr["frame_properties"]["streams"] = {
                str(k): v.asdict() for k, v in self.sensors.items()
            }

        if self.data != {}:
            dict_repr["frame_properties"]["frame_data"] = {
                "num": [v.asdict() for v in self.data.values()]
            }

        if self.object_data != {}:
            dict_repr["objects"] = {str(k): v.asdict() for k, v in self.object_data.items()}

        return dict_repr

    @classmethod
    def _prepare_data(cls, data_dict: dict) -> dict:
        """Add optional fields to dict to simplify interaction.

        Parameters
        ----------
        data_dict : dict
            JSON data.

        Returns
        -------
        dict
            Enhanced JSON data.
        """

        if "frame_properties" not in data_dict:
            data_dict["frame_properties"] = {}

        if "streams" not in data_dict["frame_properties"]:
            data_dict["frame_properties"]["streams"] = {}

        if "frame_data" not in data_dict["frame_properties"]:
            data_dict["frame_properties"]["frame_data"] = {}

        if "objects" not in data_dict:
            data_dict["objects"] = {}

        return data_dict

    def _timestamp_fromdict(data_dict: dict) -> t.Optional[decimal.Decimal]:

        if "timestamp" not in data_dict["frame_properties"]:
            return None

        return decimal.Decimal(data_dict["frame_properties"]["timestamp"])

    def _sensors_fromdict(
        data_dict: dict, frame_uid: int, scene_sensors: t.Dict[str, Sensor]
    ) -> t.Dict[str, SensorReference]:

        logger = logging.getLogger("loader_warnings")

        sensors = {}

        for sensor_id, sensor_dict in data_dict["frame_properties"]["streams"].items():
            if sensor_id not in scene_sensors:
                logger.warning(
                    f"{sensor_id} does not exist as a stream, but is referenced in the "
                    + f"sync of frame {frame_uid}."
                )
                continue

            sensors[sensor_id] = SensorReference.fromdict(
                data_dict=sensor_dict, sensor=scene_sensors[sensor_id]
            )

        return sensors

    def _frame_data_fromdict(
        data_dict: dict, frame_id: int, annotation_classes: dict, sensors: t.Dict[str, Sensor]
    ) -> t.Dict[str, Num]:

        logger = logging.getLogger("loader_warnings")

        frame_data = {}

        for ann_type in data_dict["frame_properties"]["frame_data"]:

            if ann_type not in annotation_classes:
                logger.warning(
                    f"Annotation type {ann_type} (frame {frame_id}, frame data) is "
                    + "currently not supported. Supported annotation types: "
                    + str(list(annotation_classes.keys()))
                )
                continue

            for ann_raw in data_dict["frame_properties"]["frame_data"][ann_type]:

                if "uid" not in ann_raw:
                    ann_raw["uid"] = uuid.uuid4()

                frame_data[ann_raw["name"]] = annotation_classes[ann_type].fromdict(
                    ann_raw, sensors
                )

        return frame_data

    def _objects_fromdict(
        data_dict: dict,
        frame_id: int,
        objects: t.Dict[str, Object],
        sensors: t.Dict[str, Sensor],
        annotation_classes: dict,
    ) -> t.Dict[uuid.UUID, ObjectData]:

        logger = logging.getLogger("loader_warnings")

        object_data = {}

        for obj_id, obj_ann in data_dict["objects"].items():

            if obj_id not in objects:
                logger.warning(
                    f"{obj_id} does not exist as an object, but is referenced in the object"
                    + f" annotation of frame {frame_id}."
                )
                continue

            object_data[obj_id] = ObjectData.fromdict(
                uid=obj_id,
                data_dict=obj_ann["object_data"],
                objects=objects,
                sensors=sensors,
                annotation_classes=annotation_classes,
            )

        return object_data

    def _fix_sensor_uri_attribute(frame: "Frame") -> "Frame":

        logger = logging.getLogger("loader_warnings")

        for ann_id, ann in list(frame.annotations.items()):
            for attr_name, attr_val in ann.attributes.items():

                if attr_name != "uri":
                    continue

                logger.warning(
                    f"Deprecated attribute 'uri' detected in annotation {ann_id}. The error has"
                    + " been fixed. Please update the file via 'raillabel.save()'."
                )

                frame.sensors[ann.sensor.uid].uri = attr_val
                del frame.annotations[ann_id].attributes[attr_name]
                break

        return frame

    def __eq__(self, other) -> bool:
        """Handel equal comparisons."""

        if not hasattr(other, "__dict__"):
            return False

        if len(self.__dict__) != len(other.__dict__):
            return False

        for attr in self.__dict__:

            if type(getattr(self, attr)) == type(self):
                if getattr(self, attr).uid != getattr(other, attr).uid:
                    return False

            else:
                if getattr(self, attr) != getattr(other, attr):
                    return False

        return True
