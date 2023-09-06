# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import decimal
import typing as t
import uuid
from dataclasses import dataclass, field

from ..._util._warning import _warning
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
    uid: int
        Number of the frame within the annotation file. Must be unique.
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

    uid: int
    timestamp: t.Optional[decimal.Decimal] = None
    sensors: t.Dict[str, SensorReference] = field(default_factory=dict)
    frame_data: t.Dict[str, Num] = field(default_factory=dict)
    annotations: t.Dict[str, t.Type[_ObjectAnnotation]] = field(default_factory=dict)

    @property
    def object_data(self) -> t.Dict[str, t.Dict[str, t.Type[_ObjectAnnotation]]]:
        """Return annotations categorized by Object-Id.

        Returns
        -------
        dict[str, dict[UUID, _ObjectAnnotation subclass]]
            Dictionary of annotations. Keys are object uids and values are annotations, that are
            contained in the object.
        """

        object_data = {}
        for ann_id, annotation in self.annotations.items():
            if annotation.object.uid not in object_data:
                object_data[annotation.object.uid] = {}

            object_data[annotation.object.uid][ann_id] = annotation

        return object_data

    @classmethod
    def fromdict(
        cls,
        uid: str,
        data_dict: dict,
        objects: t.Dict[str, Object],
        sensors: t.Dict[str, Sensor],
    ) -> "Frame":
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

        frame = Frame(
            uid=int(uid),
            timestamp=cls._timestamp_fromdict(data_dict),
            sensors=cls._sensors_fromdict(data_dict, int(uid), sensors),
            frame_data=cls._frame_data_fromdict(data_dict, sensors),
            annotations=cls._objects_fromdict(data_dict, int(uid), objects, sensors),
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
    def _timestamp_fromdict(cls, data_dict: dict) -> t.Optional[decimal.Decimal]:

        if "frame_properties" not in data_dict or "timestamp" not in data_dict["frame_properties"]:
            return None

        return decimal.Decimal(data_dict["frame_properties"]["timestamp"])

    @classmethod
    def _sensors_fromdict(
        cls, data_dict: dict, frame_uid: int, scene_sensors: t.Dict[str, Sensor]
    ) -> t.Dict[str, SensorReference]:

        if "frame_properties" not in data_dict or "streams" not in data_dict["frame_properties"]:
            return {}

        sensors = {}

        for sensor_id, sensor_dict in data_dict["frame_properties"]["streams"].items():
            if sensor_id not in scene_sensors:
                _warning(
                    f"{sensor_id} does not exist as a stream, but is referenced in the "
                    + f"sync of frame {frame_uid}."
                )
                continue

            sensors[sensor_id] = SensorReference.fromdict(
                data_dict=sensor_dict, sensor=scene_sensors[sensor_id]
            )

        return sensors

    @classmethod
    def _frame_data_fromdict(
        cls, data_dict: dict, sensors: t.Dict[str, Sensor]
    ) -> t.Dict[str, Num]:

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
        frame_id: int,
        objects: t.Dict[str, Object],
        sensors: t.Dict[str, Sensor],
    ) -> t.Dict[uuid.UUID, t.Type[_ObjectAnnotation]]:

        if "objects" not in data_dict:
            return {}

        annotations = {}

        for obj_id, obj_ann in data_dict["objects"].items():

            if obj_id not in objects:
                _warning(
                    f"{obj_id} does not exist as an object, but is referenced in the object"
                    + f" annotation of frame {frame_id}."
                )
                continue

            object_annotations = cls._object_annotations_fromdict(
                data_dict=obj_ann["object_data"],
                object=objects[obj_id],
                sensors=sensors,
            )

            for annotation in object_annotations:
                if annotation.uid in annotations:
                    cls._issue_duplicate_annotation_uid_warning(annotation.uid, frame_id)
                    annotation.uid = str(uuid.uuid4())

                annotations[annotation.uid] = annotation

        return annotations

    @classmethod
    def _object_annotations_fromdict(
        cls,
        data_dict: dict,
        object: Object,
        sensors: t.Dict[str, Sensor],
    ) -> t.Iterator[t.Type[_ObjectAnnotation]]:

        for ann_type, annotations_raw in data_dict.items():
            for ann_raw in annotations_raw:

                ann_raw = cls._fix_deprecated_annotation_name(ann_raw, ann_type, object.type)

                yield annotation_classes()[ann_type].fromdict(ann_raw, sensors, object)

    @classmethod
    def _fix_sensor_uri_attribute(cls, frame: "Frame") -> "Frame":

        for ann_id, ann in list(frame.annotations.items()):
            for attr_name, attr_val in ann.attributes.items():

                if attr_name != "uri":
                    continue

                _warning(
                    f"Deprecated attribute 'uri' detected in annotation {ann_id}. The error has"
                    + " been fixed. Please update the file via 'raillabel.save()'."
                )

                frame.sensors[ann.sensor.uid].uri = attr_val
                del frame.annotations[ann_id].attributes[attr_name]
                break

        return frame

    @classmethod
    def _fix_deprecated_annotation_name(cls, ann_raw: dict, ann_type: str, obj_type: str) -> dict:

        if "uid" not in ann_raw:
            try:
                ann_raw["uid"] = str(uuid.UUID(ann_raw["name"]))
            except ValueError:
                ann_raw["uid"] = str(uuid.uuid4())

        ann_raw["name"] = f"{ann_raw['coordinate_system']}__{ann_type}__{obj_type}"

        return ann_raw

    @classmethod
    def _issue_duplicate_annotation_uid_warning(cls, ann_uid: str, frame_id: int):
        _warning(
            f"Annotation UID '{ann_uid}' is contained more than once in frame {frame_id}. "
            + "A new uid will be assigned."
        )

    def _annotations_asdict(self) -> dict:
        annotations_dict = {}
        for object_id, annotations in self.object_data.items():
            annotations_dict[object_id] = {"object_data": {}}

            for annotation in annotations.values():
                if annotation.OPENLABEL_ID not in annotations_dict[object_id]["object_data"]:
                    annotations_dict[object_id]["object_data"][annotation.OPENLABEL_ID] = []

                annotations_dict[object_id]["object_data"][annotation.OPENLABEL_ID].append(
                    annotation.asdict()
                )

        return annotations_dict

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
