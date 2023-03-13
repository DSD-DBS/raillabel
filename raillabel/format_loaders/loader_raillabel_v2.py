# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import decimal
import json
import typing as t
import uuid
from pathlib import Path

from .. import exceptions, format
from ._loader_abc import LoaderABC


class LoaderRailLabelV2(LoaderABC):
    """Loader class for the OpenLabel v1 annotation format.

    Attributes
    ----------
    scene: raillabel.Scene
        Loaded raillabel.Scene with the data.
    warnings: list[str]
        List of warning strings, that have been found during the execution of load().
    """

    scene: format.Scene
    warnings: t.List[str]

    SCHEMA_PATH: Path = Path(__file__).parent.parent / "schemas" / "raillabel_v2_schema.json"

    _OPENLABEL_CLASS_MAPPING = {
        "bbox": format.Bbox,
        "cuboid": format.Cuboid,
        "num": format.Num,
        "poly2d": format.Poly2d,
        "poly3d": format.Poly3d,
        "vec": format.Seg3d,
    }

    @property
    def subschema_version(self):
        """Return subschema version."""
        with self.SCHEMA_PATH.open() as schema_file:
            subschema_version = json.load(schema_file)["version"]
        return subschema_version

    def load(self, data: dict, validate: bool = True) -> format.Scene:
        """Load the data into a raillabel.Scene and return it.

        Parameters
        ----------
        data: dict
            A dictionary loaded from a JSON-file.
        validate: bool
            If True, the annotation data is validated via the respective schema. This is highly
            recommended, as not validating the data may lead to Errors during loading or while handling
            the scene. However, validating may increase the loading time. Default is True.

        Returns
        -------
        scene: raillabel.Scene
            The loaded scene with the data.

        Raises
        ------
        raillabel.exceptions.SchemaError
            if validate is True and the data does not validate against the schema.
        """

        self.warnings = []

        if validate:
            self.validate(data)

        data = self._prepare_data(data)

        self.scene = format.Scene(
            metadata=format.Metadata.fromdict(
                data_dict=data["metadata"], subschema_version=self.subschema_version
            )
        )

        self._check_sensor_completeness(data["coordinate_systems"], data["streams"])

        for stream_id in data["streams"]:
            self.scene.sensors[stream_id] = format.Sensor.fromdict(
                uid=stream_id,
                cs_raw=data["coordinate_systems"][stream_id],
                stream_raw=data["streams"][stream_id],
            )

        for object_id in data["objects"]:
            self.scene.objects[object_id] = format.Object.fromdict(
                data["objects"][object_id], object_id
            )

        self._load_frames(data)

        return self.scene

    def supports(self, data: dict) -> bool:
        """Determine if the loader is suitable for the data (lightweight).

        Parameters
        ----------
        data: dict
            A dictionary loaded from a JSON-file.

        Returns
        -------
        bool:
            If True, the Loader class is suitable for the data.
        """

        if "subschema_version" in data["openlabel"]["metadata"]:
            return (
                "openlabel" in data
                and "metadata" in data["openlabel"]
                and "schema_version" in data["openlabel"]["metadata"]
                and data["openlabel"]["metadata"]["subschema_version"].startswith("2.")
            )

        else:
            return (
                "openlabel" in data
                and "metadata" in data["openlabel"]
                and "schema_version" in data["openlabel"]["metadata"]
            )

    # === Sub-functions for better readibility --- #

    def _load_frames(self, data: dict):

        # Iterates over the frames
        for uid, frame in data["frames"].items():

            # frame.uid and frame.timestamp
            self.scene.frames[int(uid)] = format.Frame(uid=int(uid))

            if "frame_properties" not in frame:
                frame["frame_properties"] = {}

            if "timestamp" in frame["frame_properties"]:
                self.scene.frames[int(uid)].timestamp = decimal.Decimal(
                    frame["frame_properties"]["timestamp"]
                )

            # frame.sensors
            if "streams" in frame["frame_properties"]:

                for sensor_uid, sensor in frame["frame_properties"]["streams"].items():

                    # Older version store the stream timestamp under stream_sync. This adressed here.
                    if "stream_sync" in sensor["stream_properties"]:
                        sensor["stream_properties"]["sync"] = sensor["stream_properties"][
                            "stream_sync"
                        ]

                        warning_message = f"Deprecated field 'stream_sync' in frame {uid}. Please update file with raillable.save()."
                        if warning_message not in self.warnings:
                            self.warnings.append(warning_message)

                    try:
                        self.scene.frames[int(uid)].sensors[sensor_uid] = format.SensorReference(
                            sensor=self.scene.sensors[sensor_uid],
                            timestamp=decimal.Decimal(
                                sensor["stream_properties"]["sync"]["timestamp"]
                            ),
                        )

                    except KeyError:
                        self.warnings.append(
                            f"{sensor_uid} does not exist as a stream, but is referenced in the "
                            + f"sync of frame {uid}."
                        )

                    else:
                        if "uri" in sensor:
                            self.scene.frames[int(uid)].sensors[sensor_uid].uri = sensor["uri"]

            # frame.data
            if "frame_data" in frame["frame_properties"]:

                # Iterates over the annotation types
                for ann_type in frame["frame_properties"]["frame_data"]:

                    # Raises a warnings, if the annotation type is not supported
                    if ann_type not in self._OPENLABEL_CLASS_MAPPING:
                        self.warnings.append(
                            f"Annotation type {ann_type} (frame {uid}, object {obj_uid}) is "
                            + "currently not supported."
                        )
                        continue

                    # Collects the converted annotations
                    annotations = format.AnnotationContainer()
                    for ann_raw in frame["frame_properties"]["frame_data"][ann_type]:

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
                            self.warnings.append(
                                f"Annotation '{ann_raw['uid']}' is contained more than one time "
                                + f"in frame '{uid}'. A new UID is beeing assigned."
                            )
                            ann_raw["uid"] = str(uuid.uuid4())

                        # Converts the annotation
                        (annotations[ann_raw["uid"]], w,) = self._OPENLABEL_CLASS_MAPPING[
                            ann_type
                        ].fromdict(ann_raw, self.scene.sensors)
                        self.warnings.extend(w)

                    # Allocates the annotations to the frame
                    self.scene.frames[int(uid)].data = annotations

            # Iterates over the objects in the frame
            if "objects" in frame:
                for obj_uid, obj_ann in frame["objects"].items():

                    obj_ann = obj_ann["object_data"]

                    # frame.object_data
                    try:
                        self.scene.frames[int(uid)].object_data[obj_uid] = format.ObjectData(
                            object=self.scene.objects[obj_uid]
                        )

                    except KeyError:
                        self.warnings.append(
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
                            self.warnings.append(
                                f"Annotation type {ann_type} (frame {uid}, object {obj_uid}) is "
                                + "currently not supported."
                            )
                            continue

                        # Collects the converted annotations
                        for ann_raw in obj_ann[ann_type]:

                            ann_raw = self._correct_annotation_name(ann_raw, ann_type, obj_uid)

                            # Older versions store the URI attribute in the annotation attributes.
                            # This needs to be corrected if it is the case.
                            if "attributes" in ann_raw and "text" in ann_raw["attributes"]:
                                for i, attr in enumerate(ann_raw["attributes"]["text"]):
                                    if attr["name"] == "uri":
                                        self.scene.frames[int(uid)].sensors[
                                            ann_raw["coordinate_system"]
                                        ].uri = attr["val"]
                                        del ann_raw["attributes"]["text"][i]
                                        break

                            # Raises a warning, if a duplicate annotation is detected
                            if (
                                ann_raw["uid"]
                                in self.scene.frames[int(uid)].object_data[obj_uid].annotations
                            ):
                                self.warnings.append(
                                    f"Annotation '{ann_raw['uid']}' is contained more than one "
                                    + f"time in frame '{uid}'. A new UID is beeing assigned."
                                )
                                ann_raw["uid"] = str(uuid.uuid4())

                            # Converts the annotation
                            (
                                self.scene.frames[int(uid)]
                                .object_data[obj_uid]
                                .annotations[ann_raw["uid"]],
                                w,
                            ) = self._OPENLABEL_CLASS_MAPPING[ann_type].fromdict(
                                ann_raw,
                                self.scene.sensors,
                            )
                            self.warnings.extend(w)

    def _prepare_data(self, data: dict) -> dict:
        """Add optional fields to dict and simplify interaction.

        Parameters
        ----------
        data : dict
            JSON data.

        Returns
        -------
        dict
            Enhanced JSON data.
        """

        if "coordinate_systems" not in data["openlabel"]:
            data["openlabel"]["coordinate_systems"] = {}

        if "streams" not in data["openlabel"]:
            data["openlabel"]["streams"] = {}

        if "objects" not in data["openlabel"]:
            data["openlabel"]["objects"] = {}

        if "frames" not in data["openlabel"]:
            data["openlabel"]["frames"] = {}

        return data["openlabel"]

    def _check_sensor_completeness(self, cs_data: dict, stream_data: dict):
        """Check for corresponding cs and stream completeness.

        Parameters
        ----------
        cs_data : dict
            Coordinate system data in the RailLabel format.
        stream_data : dict
            Stream data in the RailLabel format.

        Raises
        ------
        raillabel.exceptions.MissingCoordinateSystemError
            if a stream has no corresponding coordinate system.
        raillabel.exceptions.MissingStreamError
            if a coordinate system has no corresponding stream.
        raillabel.exceptions.UnsupportedParentError
            if a coordinate system has no corresponding stream.
        """

        for stream_uid in stream_data:
            if stream_uid not in cs_data:
                raise exceptions.MissingCoordinateSystemError(
                    f"Stream {stream_uid} has no corresponding coordinate system."
                )

        for cs_uid in cs_data:
            if cs_uid == "base":
                continue

            if cs_data[cs_uid]["parent"] != "base":
                raise exceptions.UnsupportedParentError(
                    f"Only 'base' is permitted as a parent for coordinate system {cs_uid}, "
                    + f"not {cs_data[cs_uid]['parent']}."
                )

            if cs_uid not in stream_data:
                raise exceptions.MissingStreamError(
                    f"Coordinate sytem {cs_uid} has no corresponding stream."
                )

    def _correct_annotation_name(
        self, ann_raw: dict, ann_type: str, obj_uid: str
    ) -> t.Tuple[dict, t.List[str]]:

        if "uid" not in ann_raw:
            try:
                ann_raw["uid"] = str(uuid.UUID(ann_raw["name"]))
            except ValueError:
                ann_raw["uid"] = str(uuid.uuid4())

        ann_raw[
            "name"
        ] = f"{ann_raw['coordinate_system']}__{ann_type}__{self.scene.objects[obj_uid].type}"

        return ann_raw
