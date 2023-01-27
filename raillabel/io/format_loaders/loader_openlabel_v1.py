# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import decimal
import typing as t
import uuid
from pathlib import Path

from ... import format
from ...exceptions import SchemaError
from ._loader_abc import LoaderABC


class LoaderOpenLabelV1(LoaderABC):
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

    SCHEMA_PATH: Path = Path(__file__).parent.parent / "schemas" / "openlabel_v1_schema.json"

    _OPENLABEL_CLASS_MAPPING = {
        "bbox": {
            "class": format.Bbox,
            "attribute_name": "bboxs",
        },
        "cuboid": {"class": format.Cuboid, "attribute_name": "cuboids"},
        "poly2d": {"class": format.Poly2d, "attribute_name": "poly2ds"},
        "vec": {"class": format.Seg3d, "attribute_name": "seg3ds"},
        "num": {"class": format.Num, "attribute_name": "nums"},
    }
    """Mapping between the OpenLABEL annotation type names and the classes / raillabel
        attribute names"""

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
        self._load_streams(data["openlabel"])
        self._load_coordinate_systems(data["openlabel"])
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
        with (Path(__file__).parent.parent.parent / "__init__.py").open() as f:
            exporter_version = [line for line in f.readlines() if line.startswith("__version__ =")]

        self.scene.metadata.exporter_version = exporter_version[-1].split('"')[1]

    def _load_streams(self, data: dict):

        # Iterates over the scenes streams
        for uid, stream in data["streams"].items():

            # stream.uid and stream.type
            self.scene.streams[uid] = format.Stream(uid=uid, type=stream["type"])

            # stream.rostopic
            if "uri" in stream:
                self.scene.streams[uid].rostopic = stream["uri"]

            # stream.description
            if "description" in stream:
                self.scene.streams[uid].description = stream["description"]

            # stream.calibration
            if (
                "stream_properties" in stream
                and "intrinsics_pinhole" in stream["stream_properties"]
            ):

                # stream.calibration.camera_matrix and stream.calibration.distortion
                self.scene.streams[uid].calibration = format.StreamCalibration(
                    camera_matrix=tuple(
                        stream["stream_properties"]["intrinsics_pinhole"]["camera_matrix"]
                    ),
                    distortion=tuple(
                        stream["stream_properties"]["intrinsics_pinhole"]["distortion_coeffs"]
                    ),
                )

                # stream.calibration.width_px
                if "width_px" in stream["stream_properties"]["intrinsics_pinhole"]:
                    self.scene.streams[uid].calibration.width_px = stream["stream_properties"][
                        "intrinsics_pinhole"
                    ]["width_px"]

                # stream.calibration.height_px
                if "height_px" in stream["stream_properties"]["intrinsics_pinhole"]:
                    self.scene.streams[uid].calibration.height_px = stream["stream_properties"][
                        "intrinsics_pinhole"
                    ]["height_px"]

    def _load_coordinate_systems(self, data: dict):

        # As coordinate systems have a parent and a children attribute, which point to other
        # coordinate systems, they must be added to the scene without these values first to
        # ensure, that every coordinate system already exists before it is pointed to. The parent
        # and children attributes are added in the second loop.

        # Iterates over the scenes coordinate systems to create them
        for uid, cs in data["coordinate_systems"].items():

            # coordinate_system.uid and coordinate_system.type
            self.scene.coordinate_systems[uid] = format.CoordinateSystem(uid=uid, type=cs["type"])

        # Iterates over the scenes coordinate systems to add the parents and children
        for uid, cs in data["coordinate_systems"].items():

            # coordinate_system.parent
            if cs["parent"] != "":

                try:
                    self.scene.coordinate_systems[uid].parent = self.scene.coordinate_systems[
                        cs["parent"]
                    ]

                except KeyError:
                    self.warnings.append(
                        f"{cs['parent']} does not exist as a coordinate system, but is referenced as the parent of {uid}."
                    )

            # coordinate_system.children
            if "children" in cs and cs["children"] != []:

                for child_uid in cs["children"]:
                    try:
                        self.scene.coordinate_systems[uid].children[
                            child_uid
                        ] = self.scene.coordinate_systems[child_uid]

                    except KeyError:
                        self.warnings.append(
                            f"{child_uid} does not exist as a coordinate system, but is referenced as the child of {uid}."
                        )

            # coordinate_system.transform
            if (
                "pose_wrt_parent" in cs
                and "translation" in cs["pose_wrt_parent"]
                and "quaternion" in cs["pose_wrt_parent"]
            ):
                self.scene.coordinate_systems[uid].transform = format.Transform(
                    pos=format.Point3d(
                        x=cs["pose_wrt_parent"]["translation"][0],
                        y=cs["pose_wrt_parent"]["translation"][1],
                        z=cs["pose_wrt_parent"]["translation"][2],
                    ),
                    quat=format.Quaternion(
                        x=cs["pose_wrt_parent"]["quaternion"][0],
                        y=cs["pose_wrt_parent"]["quaternion"][1],
                        z=cs["pose_wrt_parent"]["quaternion"][2],
                        w=cs["pose_wrt_parent"]["quaternion"][3],
                    ),
                )

    def _load_objects(self, data: dict):

        # Iterates over the objects
        for uid, obj in data["objects"].items():

            # object.uid and object.type and object.name
            self.scene.objects[uid] = format.Object(uid=uid, type=obj["type"], name=obj["name"])

            # object.coordinate_system
            if "coordinate_system" in obj and obj["coordinate_system"] != "":
                try:
                    self.scene.objects[uid].coordinate_system = self.scene.coordinate_systems[
                        obj["coordinate_system"]
                    ]

                except KeyError:
                    self.warnings.append(
                        f"{obj['coordinate_system']} does not exist as a coordinate system, but is referenced in the object {uid}."
                    )

    def _load_frames(self, data: dict):

        # Iterates over the frames
        for uid, frame in data["frames"].items():

            # frame.uid and frame.timestamp
            self.scene.frames[int(uid)] = format.Frame(
                uid=int(uid),
                timestamp=decimal.Decimal(frame["frame_properties"]["timestamp"]),
            )

            # frame.streams
            if "streams" in frame["frame_properties"]:
                for stream_uid, stream_reference in frame["frame_properties"]["streams"].items():
                    try:
                        self.scene.frames[int(uid)].streams[stream_uid] = format.StreamReference(
                            stream=self.scene.streams[stream_uid],
                            timestamp=decimal.Decimal(
                                stream_reference["stream_properties"]["stream_sync"]["timestamp"]
                            ),
                        )

                    except KeyError:
                        self.warnings.append(
                            f"{stream_uid} does not exist as a stream, but is referenced in the "
                            + f"stream_sync of frame {uid}."
                        )

                    else:
                        if "uri" in stream_reference:
                            self.scene.frames[int(uid)].streams[stream_uid].uri = stream_reference[
                                "uri"
                            ]

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
                            continue

                        # Converts the annotation
                        (annotations[ann_raw["uid"]], w,) = self._OPENLABEL_CLASS_MAPPING[ann_type][
                            "class"
                        ].fromdict(ann_raw, self.scene.coordinate_systems)
                        self.warnings.extend(w)

                    # Allocates the annotations to the frame
                    self.scene.frames[int(uid)].data = annotations

            # Iterates over the objects in the frame
            if "objects" in frame:
                for obj_uid, obj_ann in frame["objects"].items():

                    obj_ann = obj_ann["object_data"]

                    # frame.objects
                    try:
                        self.scene.frames[int(uid)].objects[obj_uid] = format.ObjectAnnotations(
                            object=self.scene.objects[obj_uid],
                            frame=self.scene.frames[int(uid)],
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
                        annotations = {}
                        for ann_raw in obj_ann[ann_type]:

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
                                continue

                            # Converts the annotation
                            (annotations[ann_raw["uid"]], w,) = self._OPENLABEL_CLASS_MAPPING[
                                ann_type
                            ]["class"].fromdict(
                                ann_raw,
                                self.scene.coordinate_systems,
                                self.scene.frames[int(uid)].objects[obj_uid],
                            )
                            self.warnings.extend(w)

                        # Allocates the annotations to the frame-object
                        setattr(
                            self.scene.frames[int(uid)].objects[obj_uid],
                            self._OPENLABEL_CLASS_MAPPING[ann_type]["attribute_name"],
                            annotations,
                        )
