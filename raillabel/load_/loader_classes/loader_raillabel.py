# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
import typing as t
from pathlib import Path

from ... import exceptions, format
from ..._util._warning import _WarningsLogger
from ._loader_abc import LoaderABC


class LoaderRailLabel(LoaderABC):
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

    SCHEMA_PATH: Path = (
        Path(__file__).parent.parent.parent / "validate" / "schemas" / "raillabel_schema.json"
    )

    @property
    def subschema_version(self):
        """Return subschema version."""
        with self.SCHEMA_PATH.open() as schema_file:
            subschema_version = json.load(schema_file)["version"]
        return subschema_version

    def load(self, data: dict, validate: bool = False) -> format.Scene:
        """Load the data into a raillabel.Scene and return it.

        Parameters
        ----------
        data: dict
            A dictionary loaded from a JSON-file.
        validate: bool, optional
            If True, the annotation data is validated via the respective schema. This is
            recommended, if you are working with a modified or non-official file. Setting this
            option will increase loading time. Default is False.

        Returns
        -------
        scene: raillabel.Scene
            The loaded scene with the data.

        Raises
        ------
        raillabel.exceptions.SchemaError
            if validate is True and the data does not validate against the schema.
        """

        if validate:
            self.validate(data)

        with _WarningsLogger() as logger:
            self.scene = format.Scene.fromdict(data, self.subschema_version)

        self.warnings = logger.warnings

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

        if "openlabel" not in data or "metadata" not in data["openlabel"]:
            return False

        if "subschema_version" in data["openlabel"]["metadata"]:
            return (
                "openlabel" in data
                and "metadata" in data["openlabel"]
                and "schema_version" in data["openlabel"]["metadata"]
                and data["openlabel"]["metadata"]["subschema_version"].split(".")[0] in ["2", "3"]
            )

        else:
            return (
                "openlabel" in data
                and "metadata" in data["openlabel"]
                and "schema_version" in data["openlabel"]["metadata"]
            )

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
