# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import decimal
import typing as t
import uuid
from pathlib import Path

from .. import format
from ..exceptions import SchemaError
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

        # Validates the data
        if validate:

            is_data_valid, schema_errors = self.validate(data)
            if not is_data_valid:

                error_msg = (
                    "The loaded data does not validate against the schema. Errors in the schema:\n"
                )

                for err in schema_errors:
                    error_msg += " - " + err + "\n"

                raise SchemaError(error_msg)

        self.warnings = []

        # Initializes the scene
        self.scene = format.Scene(metadata=format.Metadata(schema_version="1.0.0"))

        # The code for loading the data in split into functions, that load one respective part of
        # the data. This is meant to improve readibility.

        self._load_metadata(data["openlabel"])
        self._load_sensors(data["openlabel"])
        self._load_objects(data["openlabel"])
        self._load_frames(data["openlabel"])

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

        return (
            "openlabel" in data
            and "metadata" in data["openlabel"]
            and "schema_version" in data["openlabel"]["metadata"]
            and data["openlabel"]["metadata"]["schema_version"].startswith("1.")
        )

    # === Sub-functions for better readibility --- #

    def _load_metadata(self, data: dict):

        # metadata.file_version
        if "file_version" in data["metadata"]:
            self.scene.metadata.file_version = data["metadata"]["file_version"]

        # metadata.name
        if "name" in data["metadata"]:
            self.scene.metadata.name = data["metadata"]["name"]

        # metadata.tagged_file
        if "tagged_file" in data["metadata"]:
            self.scene.metadata.tagged_file = data["metadata"]["tagged_file"]

        # metadata.comment
        if "comment" in data["metadata"]:
            self.scene.metadata.comment = data["metadata"]["comment"]

        # metadata.exporter_version

        # Version of the raillabel-devkit can not be imported due to circular imports and therefore
        # needs to be read from the __init__.py file directly.
        with (Path(__file__).parent.parent / "__init__.py").open() as f:
            exporter_version = [line for line in f.readlines() if line.startswith("__version__ =")]

        self.scene.metadata.exporter_version = exporter_version[-1].split('"')[1]

    def _load_sensors(self, data: dict):

        for stream_id, stream_raw in data["streams"].items():

            if stream_id not in data["coordinate_systems"]:
                self.warnings.append(f"Stream {stream_id} has no corresponding coordinate system.")
                data["coordinate_systems"][stream_id] = {"parent": "base"}

            cs_raw = data["coordinate_systems"][stream_id]

            self.scene.sensors[stream_id], w = format.Sensor.fromdict(stream_id, cs_raw, stream_raw)
            self.warnings.extend(w)

    def _load_objects(self, data: dict):

        # Iterates over the objects
        for uid, obj in data["objects"].items():

            # object.uid and object.type and object.name
            self.scene.objects[uid] = format.Object(uid=uid, type=obj["type"], name=obj["name"])

    def _load_frames(self, data: dict):

        # Iterates over the frames
        for uid, frame in data["frames"].items():

            # frame.uid and frame.timestamp
            self.scene.frames[int(uid)] = format.Frame(
                uid=int(uid),
                timestamp=decimal.Decimal(frame["frame_properties"]["timestamp"]),
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
                                f"Annotation {ann_raw['uid']} is contained more than one time "
                                + f"in frame {uid}."
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

                            # Older versions have the annotation UUID stored in the 'name' field.
                            # This needs to be corrected first.
                            if not "uid" in ann_raw:
                                try:
                                    ann_raw["uid"] = str(uuid.UUID(ann_raw["name"]))
                                except ValueError:
                                    ann_raw["uid"] = str(uuid.uuid4())
                                else:
                                    ann_raw["name"] = "general"

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
                                    f"Annotation {ann_raw['uid']} is contained more than one time "
                                    + f"in frame {uid}."
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
