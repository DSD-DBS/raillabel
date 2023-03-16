# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import decimal
import typing as t
import uuid
from dataclasses import dataclass, field

from .num import Num
from .object import Object
from .object_data import (  # TODO
    AnnotationContainer,
    Bbox,
    Cuboid,
    ObjectData,
    Poly2d,
    Poly3d,
    Seg3d,
)
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

    _OPENLABEL_CLASS_MAPPING = {  #  TODO
        "bbox": Bbox,
        "cuboid": Cuboid,
        "num": Num,
        "poly2d": Poly2d,
        "poly3d": Poly3d,
        "vec": Seg3d,
    }

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
        self, uid: str, data_dict: dict, objects: t.Dict[str, Object], sensors: t.Dict[str, Sensor]
    ):
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

        Returns
        -------
        frame: raillabel.format.Frame
            Converted Frame object.
        warnings: list of str
            List of warnings, that occurred during execution.
        """

        data_dict = self._prepare_data(data_dict)

        frame = Frame(int(uid))
        warnings = []

        if "timestamp" in data_dict["frame_properties"]:
            frame.timestamp = decimal.Decimal(data_dict["frame_properties"]["timestamp"])

        for sensor_id, sensor_dict in data_dict["frame_properties"]["streams"].items():
            if sensor_id not in sensors:
                warnings.append(
                    f"{sensor_id} does not exist as a stream, but is referenced in the "
                    + f"sync of frame {uid}."
                )
                continue

            frame.sensors[sensor_id], w = SensorReference.fromdict(
                data_dict=sensor_dict, sensor=sensors[sensor_id]
            )
            warnings.extend(w)

        # frame.data
        for ann_type in data_dict["frame_properties"]["frame_data"]:

            # Raises a warnings, if the annotation type is not supported
            if ann_type not in self._OPENLABEL_CLASS_MAPPING:
                warnings.append(
                    f"Annotation type {ann_type} (frame {uid}, object {obj_uid}) is "
                    + "currently not supported."
                )
                continue

            # Collects the converted annotations
            annotations = AnnotationContainer()
            for ann_raw in data_dict["frame_properties"]["frame_data"][ann_type]:

                # Older version have the annotation UUID stored in the 'name' field. This
                # needs to be corrected first.
                if not "uid" in ann_raw:
                    try:
                        ann_raw["uid"] = str(uuid.UUID(ann_raw["name"]))
                    except ValueError:
                        ann_raw["uid"] = str(uuid.uuid4())
                    else:
                        ann_raw["name"] = "general"

                # Raises a warning, if a duplicate annotation is detected
                if ann_raw["uid"] in annotations:
                    warnings.append(
                        f"Annotation '{ann_raw['uid']}' is contained more than one time "
                        + f"in frame '{uid}'. A new UID is beeing assigned."
                    )
                    ann_raw["uid"] = str(uuid.uuid4())

                # Converts the annotation
                (annotations[ann_raw["uid"]], w,) = self._OPENLABEL_CLASS_MAPPING[
                    ann_type
                ].fromdict(ann_raw, sensors)
                warnings.extend(w)

            # Allocates the annotations to the frame
            frame.data = annotations

        # Iterates over the objects in the frame
        for obj_uid, obj_ann in data_dict["objects"].items():

            obj_ann = obj_ann["object_data"]

            # frame.object_data
            try:
                frame.object_data[obj_uid] = ObjectData(object=objects[obj_uid])

            except KeyError:
                warnings.append(
                    f"{obj_uid} does not exist as an object, but is referenced in the object"
                    + f" annotation of frame {uid}."
                )
                continue

            # Since there are a lot of annotation types, that all require unique methods for
            # parsing the data from the OpenLABEL format, the parsing is handed off to the
            # individual data classes via the fromdict() method. The mapping of the OpenLABEL
            # annotation types to the classes is performend via the openlable_class_mapping
            # dict.

            # Iterates over the annotation types
            for ann_type in obj_ann:

                # Raises a warnings, if the annotation type is not supported
                if ann_type not in self._OPENLABEL_CLASS_MAPPING:
                    warnings.append(
                        f"Annotation type {ann_type} (frame {uid}, object {obj_uid}) is "
                        + "currently not supported."
                    )
                    continue

                # Collects the converted annotations
                for ann_raw in obj_ann[ann_type]:

                    ann_raw = self._correct_annotation_name(
                        ann_raw, ann_type, objects[obj_uid].type
                    )

                    # Older versions store the URI attribute in the annotation attributes.
                    # This needs to be corrected if it is the case.
                    if "attributes" in ann_raw and "text" in ann_raw["attributes"]:
                        for i, attr in enumerate(ann_raw["attributes"]["text"]):
                            if attr["name"] == "uri":
                                frame.sensors[ann_raw["coordinate_system"]].uri = attr["val"]
                                del ann_raw["attributes"]["text"][i]
                                break

                    # Raises a warning, if a duplicate annotation is detected
                    if ann_raw["uid"] in frame.object_data[obj_uid].annotations:
                        warnings.append(
                            f"Annotation '{ann_raw['uid']}' is contained more than one "
                            + f"time in frame '{uid}'. A new UID is beeing assigned."
                        )
                        ann_raw["uid"] = str(uuid.uuid4())

                    # Converts the annotation
                    (
                        frame.object_data[obj_uid].annotations[ann_raw["uid"]],
                        w,
                    ) = self._OPENLABEL_CLASS_MAPPING[ann_type].fromdict(
                        ann_raw,
                        sensors,
                    )
                    warnings.extend(w)

        return frame, warnings

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

    def _prepare_data(data_dict: dict) -> dict:
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

    def _correct_annotation_name(
        ann_raw: dict, ann_type: str, obj_type: str
    ) -> t.Tuple[dict, t.List[str]]:

        if "uid" not in ann_raw:
            try:
                ann_raw["uid"] = str(uuid.UUID(ann_raw["name"]))
            except ValueError:
                ann_raw["uid"] = str(uuid.uuid4())

        ann_raw["name"] = f"{ann_raw['coordinate_system']}__{ann_type}__{obj_type}"

        return ann_raw

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
