# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
import uuid
from dataclasses import dataclass, field
from decimal import Decimal

from .bbox import Bbox
from .coordinate_system import CoordinateSystem
from .cuboid import Cuboid
from .frame import Frame
from .metadata import Metadata
from .object import Object
from .object_data import ObjectData
from .poly2d import Poly2d
from .seg3d import Seg3d
from .stream import Stream
from .stream_reference import StreamReference


@dataclass
class Scene:
    """The root RailLabel class, which contains all data.

    Parameters
    ----------
    metadata: raillabel.format.Metadata
        This object contains information, that is, metadata, about the annotation file itself.
    streams: dict of raillabel.format.Stream, optional
        Dictionary of raillabel.format.Streams. Dictionary keys are the stream uids. Default is {}.
    coordinate_systems: dict of raillabel.format.CoordinateSystem, optional
        Dictionary of raillabel.format.CoordinateSystems. Dictionary keys are the coordinate_system
        uids. Default is {}.
    objects: dict of raillabel.format.Object, optional
        Dictionary of raillabel.format.Objects. Dictionary keys are the object uids. Default is {}.
    frames: dict of raillabel.format.Frame, optional
        Dict of frames in the scene. Dictionary keys are the frame uids. Default is {}.
    """

    metadata: Metadata
    streams: t.Dict[str, Stream] = field(default_factory=dict)
    coordinate_systems: t.Dict[str, CoordinateSystem] = field(default_factory=dict)
    objects: t.Dict[uuid.UUID, Object] = field(default_factory=dict)
    frames: t.Dict[int, Frame] = field(default_factory=dict)

    def asdict(self) -> dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this Scene.

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.
        """

        dict_repr = {"openlabel": {"metadata": self.metadata.asdict()}}

        if self.streams != {}:
            dict_repr["openlabel"]["streams"] = {
                str(k): v.asdict() for k, v in self.streams.items()
            }

        if self.coordinate_systems != {}:
            dict_repr["openlabel"]["coordinate_systems"] = {
                str(k): v.asdict() for k, v in self.coordinate_systems.items()
            }

        if self.objects != {}:
            dict_repr["openlabel"]["objects"] = {
                str(k): v.asdict() for k, v in self.objects.items()
            }

        if self.frames != {}:
            dict_repr["openlabel"]["frames"] = {str(k): v.asdict() for k, v in self.frames.items()}

        return dict_repr

    def filter(
        self,
        include_annotation_ids: t.List[str] = [],
        exclude_annotation_ids: t.List[str] = [],
        include_annotation_types: t.List[str] = [],
        exclude_annotation_types: t.List[str] = [],
        include_attributes: dict = {},
        exclude_attributes: dict = {},
        include_classes: t.List[str] = [],
        exclude_classes: t.List[str] = [],
        include_frames: t.List[int] = [],
        exclude_frames: t.List[int] = [],
        start_frame: int = -1,
        end_frame: int = float("inf"),
        start_timestamp: Decimal = -1,
        end_timestamp: Decimal = float("inf"),
        include_object_ids: t.List[str] = [],
        exclude_object_ids: t.List[str] = [],
        include_sensors: t.List[str] = [],
        exclude_sensors: t.List[str] = [],
    ) -> "Scene":
        """Return a copy of the scene with the annotations filtered.

        Parameters
        ----------
        include_classes: str or list of str
            List of class/type names that should be included in the filtered scene. If set, no
            other classes/types will be copied. Mutually exclusive with exclude_classes.
        exclude_classes: str or list of str
            List of class/type names that should be excluded in the filtered scene. If set, all
            other classes/types will be copied. Mutually exclusive with include_classes.
        include_annotation_types: str or list of str
            List of annotation types (i.e. bboxs, cuboids, poly2ds, seg3ds) that should be included
            in the filtered scene. If set, no other annotation types will be copied. Mutually
            exclusive with exclude_annotation_types.
        exclude_annotation_types: str or list of str
            List of annotation types (i.e. bboxs, cuboids, poly2ds, seg3ds) that should be excluded
            in the filtered scene. If set, all other annotation types will be copied. Mutually
            exclusive with include_annotation_types.
        include_annotation_ids: str or list of str
            List of annotation UIDs that should be included in the filtered scene. If set, no other
            annotation UIDs will be copied. Mutually exclusive with exclude_annotation_ids.
        exclude_annotation_ids: str or list of str
            List of annotation UIDs that should be excluded in the filtered scene. If set, all
            other annotation UIDs will be copied. Mutually exclusive with include_annotation_ids.
        include_object_ids: str or list of str
            List of object UIDs that should be included in the filtered scene. If set, no other
            objects will be copied. Mutually exclusive with exclude_object_ids.
        exclude_object_ids: str or list of str
            List of object UIDs that should be excluded in the filtered scene. If set, all other
            objects will be copied. Mutually exclusive with include_object_ids.
        include_sensors: str or list of str
            List of sensors that should be included in the filtered scene. If set, no other
            sensors will be copied. Mutually exclusive with exclude_sensors.
        exclude_sensors: str or list of str
            List of sensors that should be excluded in the filtered scene. If set, all other
            sensors will be copied. Mutually exclusive with include_sensors.
        include_attributes: dict
            Dict of attributes that should be included in the filtered scene. Dict keys are the
            attribute names, values are the specific values that should be included. If the
            value is set so None, all annotations with the attribute are included regardless of
            value. Mutually exclusive with exclude_attributes.
        exclude_attributes: dict
            Dict of attributes that should be excluded in the filtered scene. Dict keys are the
            attribute names, values are the specific values that should be excluded. If the value
            is set so None, all annotations with the attribute are excluded regardless of value.
            Mutually exclusive with include_attributes.
        include_frames: int or list of int
            List of frame UIDs that should be included in the filtered scene. If set, no other
            frames will be copied. Mutually exclusive with exclude_frames.
        exclude_frames: int or list of int
            List of frame UIDs that should be excluded in the filtered scene. If set, all other
            frames will be copied. Mutually exclusive with include_frames.
        start_frame: int
            Frame at which the filtered scene should start. Mutually exclusive with s
            tart_timestamp.
        end_frame: int
            Frame at which the filtered scene should end (inclusive). Mutually exclusive with
            end_timestamp.
        start_timestamp: decimal.Decimal
            Unix timestamp at which the filtered scene should start (inclusive). Mutually exclusive
            with start_frame.
        end_timestamp: decimal.Decimal
            Unix timestamp at which the filtered scene should end (inclusive). Mutually exclusive
            with end_frame.

        Raises
        ------
        ValueError
            if two mutually exclusive parameters are set.
        """

        # Preprocesses the parameters and raises and Error if mutually exclusive parameters are set
        if isinstance(include_annotation_ids, str):
            include_annotation_ids = [include_annotation_ids]
        else:
            include_annotation_ids = list(include_annotation_ids)

        if isinstance(exclude_annotation_ids, str):
            exclude_annotation_ids = [exclude_annotation_ids]
        else:
            exclude_annotation_ids = list(exclude_annotation_ids)

        if len(include_annotation_ids) > 0 and len(exclude_annotation_ids) > 0:
            raise ValueError(
                "The include_annotation_ids and exclude_annotation_ids parameters are mutually exclusive."
            )

        if isinstance(include_annotation_types, str):
            include_annotation_types = [include_annotation_types]
        else:
            include_annotation_types = list(include_annotation_types)

        if isinstance(exclude_annotation_types, str):
            exclude_annotation_types = [exclude_annotation_types]
        else:
            exclude_annotation_types = list(exclude_annotation_types)

        if len(include_annotation_types) > 0 and len(exclude_annotation_types) > 0:
            raise ValueError(
                "The include_annotation_types and exclude_annotation_types parameters are mutually exclusive."
            )

        if len(include_attributes) > 0 and len(exclude_attributes) > 0:
            raise ValueError(
                "The include_attributes and exclude_attributes parameters are mutually exclusive."
            )

        if isinstance(include_classes, str):
            include_classes = [include_classes]
        else:
            include_classes = list(include_classes)

        if isinstance(exclude_classes, str):
            exclude_classes = [exclude_classes]
        else:
            exclude_classes = list(exclude_classes)

        if len(include_classes) > 0 and len(exclude_classes) > 0:
            raise ValueError(
                "The include_classes and exclude_classes parameters are mutually exclusive."
            )

        if isinstance(include_frames, int):
            include_frames = [include_frames]
        else:
            include_frames = list(include_frames)

        for i in range(len(include_frames)):
            include_frames[i] = int(include_frames[i])

        if isinstance(exclude_frames, int):
            exclude_frames = [exclude_frames]
        else:
            exclude_frames = list(exclude_frames)

        for i in range(len(exclude_frames)):
            exclude_frames[i] = int(exclude_frames[i])

        if len(include_frames) > 0 and len(exclude_frames) > 0:
            raise ValueError(
                "The include_frames and exclude_frames parameters are mutually exclusive."
            )

        if start_frame != -1:
            start_frame = int(start_frame)

        if start_timestamp != -1:
            start_timestamp = Decimal(start_timestamp)

        if start_frame != -1 and start_timestamp != -1:
            raise ValueError(
                "The start_frame and start_timestamp parameters are mutually exclusive."
            )

        if end_frame != float("inf"):
            end_frame = int(end_frame)

        if end_timestamp != float("inf"):
            end_timestamp = Decimal(end_timestamp)

        if end_frame != float("inf") and end_timestamp != float("inf"):
            raise ValueError("The end_frame and end_timestamp parameters are mutually exclusive.")

        if isinstance(include_object_ids, str):
            include_object_ids = [include_object_ids]
        else:
            include_object_ids = list(include_object_ids)

        if isinstance(exclude_object_ids, str):
            exclude_object_ids = [exclude_object_ids]
        else:
            exclude_object_ids = list(exclude_object_ids)

        if len(include_object_ids) > 0 and len(exclude_object_ids) > 0:
            raise ValueError(
                "The include_object_ids and exclude_object_ids parameters are mutually exclusive."
            )

        if isinstance(include_sensors, str):
            include_sensors = [include_sensors]
        else:
            include_sensors = list(include_sensors)

        if isinstance(exclude_sensors, str):
            exclude_sensors = [exclude_sensors]
        else:
            exclude_sensors = list(exclude_sensors)

        if len(include_sensors) > 0 and len(exclude_sensors) > 0:
            raise ValueError(
                "The include_sensors and exclude_sensors parameters are mutually exclusive."
            )

        # Variables for tracking used sensors
        used_sensors = []

        # Creates the return scene
        filtered_scene = Scene(
            metadata=self.metadata,
            coordinate_systems={"base": CoordinateSystem(uid="base", parent=None, type="local")},
        )

        # Iterates over the frames
        for frame in self.frames.values():

            # Skips the iteration if the frame should be omitted
            if frame.uid < start_frame or frame.uid > end_frame:
                continue

            if frame.timestamp < Decimal(start_timestamp) or frame.timestamp > Decimal(
                end_timestamp
            ):
                continue

            if (
                frame.uid not in include_frames and len(include_frames) > 0
            ) or frame.uid in exclude_frames:
                continue

            # Iterates over the objects
            for obj_uid, obj in frame.object_data.items():

                # Skips the iteration if the object should be omitted
                if (
                    obj.object.type not in include_classes and len(include_classes) > 0
                ) or obj.object.type in exclude_classes:
                    continue

                if (
                    obj_uid not in include_object_ids and len(include_object_ids) > 0
                ) or obj_uid in exclude_object_ids:
                    continue

                # As the annotations are dispersed over multiple variables in ObjectAnnotation,
                # they are concatinated to a single dict for writing the code only once.
                anns = {}

                if (
                    len(include_annotation_types) == 0
                    and len(exclude_annotation_types) == 0
                    or "bbox" in include_annotation_types
                    or "bboxs" in include_annotation_types
                    or (
                        len(exclude_annotation_types) > 0
                        and "bbox" not in exclude_annotation_types
                        and "bboxs" not in exclude_annotation_types
                    )
                ):
                    anns.update(obj.bboxs)

                if (
                    len(include_annotation_types) == 0
                    and len(exclude_annotation_types) == 0
                    or "poly2d" in include_annotation_types
                    or "poly2ds" in include_annotation_types
                    or (
                        len(exclude_annotation_types) > 0
                        and "poly2d" not in exclude_annotation_types
                        and "poly2ds" not in exclude_annotation_types
                    )
                ):
                    anns.update(obj.poly2ds)

                if (
                    len(include_annotation_types) == 0
                    and len(exclude_annotation_types) == 0
                    or "cuboid" in include_annotation_types
                    or "cuboids" in include_annotation_types
                    or (
                        len(exclude_annotation_types) > 0
                        and "cuboid" not in exclude_annotation_types
                        and "cuboids" not in exclude_annotation_types
                    )
                ):
                    anns.update(obj.cuboids)

                if (
                    len(include_annotation_types) == 0
                    and len(exclude_annotation_types) == 0
                    or "seg3d" in include_annotation_types
                    or "seg3ds" in include_annotation_types
                    or (
                        len(exclude_annotation_types) > 0
                        and "seg3d" not in exclude_annotation_types
                        and "seg3ds" not in exclude_annotation_types
                    )
                ):
                    anns.update(obj.seg3ds)

                # Iterates over the annotations
                for ann in anns.values():

                    if (
                        ann.uid not in include_annotation_ids and len(include_annotation_ids) > 0
                    ) or ann.uid in exclude_annotation_ids:
                        continue

                    if (
                        ann.coordinate_system.uid not in include_sensors
                        and len(include_sensors) > 0
                    ) or ann.coordinate_system.uid in exclude_sensors:
                        continue

                    if len(include_attributes) > 0:

                        omit_due_to_attribute = True
                        for attr_key, attr_val in ann.attributes.items():
                            if attr_key in include_attributes and (
                                include_attributes[attr_key] is None
                                or include_attributes[attr_key] == attr_val
                            ):
                                omit_due_to_attribute = False
                                break

                    elif len(exclude_attributes) > 0:

                        omit_due_to_attribute = False
                        for attr_key, attr_val in ann.attributes.items():
                            if attr_key in exclude_attributes and (
                                exclude_attributes[attr_key] is None
                                or exclude_attributes[attr_key] == attr_val
                            ):
                                omit_due_to_attribute = True
                                break

                    else:
                        omit_due_to_attribute = False

                    if omit_due_to_attribute:
                        continue

                    # This section of the loop is only reached if the annotation matches the
                    # filter criteria.

                    # Adds the frame if not already added
                    if frame.uid not in filtered_scene.frames:
                        filtered_scene.frames[frame.uid] = Frame(
                            uid=frame.uid, timestamp=frame.timestamp
                        )

                    # Adds the object, if not already added
                    if obj_uid not in filtered_scene.objects:
                        filtered_scene.objects[obj_uid] = self.objects[obj_uid]

                    # Adds the object to the frame, if not already added
                    if obj_uid not in filtered_scene.frames[frame.uid].object_data:
                        filtered_scene.frames[frame.uid].object_data[obj_uid] = ObjectData(
                            object=filtered_scene.objects[obj_uid]
                        )

                    # Adds the annotation
                    if isinstance(ann, Bbox):
                        filtered_scene.frames[frame.uid].object_data[obj_uid].bboxs[ann.uid] = ann

                    if isinstance(ann, Poly2d):
                        filtered_scene.frames[frame.uid].object_data[obj_uid].poly2ds[ann.uid] = ann

                    if isinstance(ann, Cuboid):
                        filtered_scene.frames[frame.uid].object_data[obj_uid].cuboids[ann.uid] = ann

                    if isinstance(ann, Seg3d):
                        filtered_scene.frames[frame.uid].object_data[obj_uid].seg3ds[ann.uid] = ann

                    # Stores the sensor name for adding it later
                    if not ann.coordinate_system.uid in used_sensors:
                        used_sensors.append(ann.coordinate_system.uid)

        # Adds the sensors to the scene and its frames
        for sensor_uid in used_sensors:
            filtered_scene.streams[sensor_uid] = self.streams[sensor_uid]

            filtered_scene.coordinate_systems[sensor_uid] = self.coordinate_systems[sensor_uid]
            filtered_scene.coordinate_systems["base"].children[
                sensor_uid
            ] = filtered_scene.coordinate_systems[sensor_uid]
            filtered_scene.coordinate_systems[
                sensor_uid
            ].parent = filtered_scene.coordinate_systems["base"]

        for frame_uid in filtered_scene.frames.keys():
            for sensor_uid in used_sensors:
                filtered_scene.frames[frame_uid].streams[sensor_uid] = StreamReference(
                    stream=filtered_scene.streams[sensor_uid],
                    timestamp=self.frames[frame_uid]
                    .streams[sensor_uid]
                    .timestamp,  # TODO: INCLUDE URI
                )

        return filtered_scene
