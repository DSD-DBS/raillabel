# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import typing as t
from importlib import import_module
from inspect import isclass
from io import StringIO
from pathlib import Path
from pkgutil import iter_modules

from .. import exceptions, format
from ..format._annotation import _Annotation
from ._loader_abc import LoaderABC


class LoaderRailLabelV2(LoaderABC):
    """Loader class for the OpenLabel v1 annotation format.

    Attributes
    ----------
    scene: raillabel.Scene
        Loaded raillabel.Scene with the data.
    warnings: t.List[str]
        List of warning strings, that have been found during the execution of load().
    """

    scene: format.Scene
    warnings: t.List[str]

    SCHEMA_PATH: Path = Path(__file__).parent.parent / "schemas" / "raillabel_v2_schema.json"

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

        self._set_up_logger()

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
                cs_data_dict=data["coordinate_systems"][stream_id],
                stream_data_dict=data["streams"][stream_id],
            )

        for object_id in data["objects"]:
            self.scene.objects[object_id] = format.Object.fromdict(
                data["objects"][object_id], object_id
            )

        annotation_classes = self._fetch_annotation_classes()
        for frame_id in data["frames"]:
            self.scene.frames[int(frame_id)] = format.Frame.fromdict(
                uid=frame_id,
                data_dict=data["frames"][frame_id],
                objects=self.scene.objects,
                sensors=self.scene.sensors,
                annotation_classes=annotation_classes,
            )

        self.warnings = self._get_warnings()
        self._clear_log_handler()

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

    def _set_up_logger(self) -> t.Tuple[StringIO, logging.StreamHandler]:
        """Set up the warnings logger.

        Returns
        -------
        StringIO
            stream containing the warnings.
        """

        logger = logging.getLogger("loader_warnings")
        warnings_stream = StringIO()
        handler = logging.StreamHandler(warnings_stream)
        handler.setLevel(logging.WARNING)
        logger.addHandler(handler)

        return warnings_stream

    def _prepare_data(self, data: dict) -> dict:
        """Add optional fields to dict to simplify interaction.

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

    def _fetch_annotation_classes(self) -> dict:

        annotation_classes = {}

        package_dir = str(Path(__file__).resolve().parent.parent / "format")
        for (_, module_name, _) in iter_modules([package_dir]):

            module = import_module(f"raillabel.format.{module_name}")
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)

                if (
                    isclass(attribute)
                    and issubclass(attribute, _Annotation)
                    and attribute != _Annotation
                ):
                    annotation_classes[attribute.OPENLABEL_ID] = attribute

        return annotation_classes

    def _get_warnings(self) -> t.List[str]:
        """Fetch warnings from logger as list.

        Returns
        -------
        list of str
            List of warnings.
        """

        logger = logging.getLogger("loader_warnings")
        stream = logger.handlers[-1].stream
        stream.seek(0)

        warnings_list = stream.getvalue().split("\n")

        if len(warnings_list) > 0:
            warnings_list = warnings_list[:-1]

        return warnings_list

    def _clear_log_handler(self):
        logging.getLogger("loader_warnings").handlers = []
