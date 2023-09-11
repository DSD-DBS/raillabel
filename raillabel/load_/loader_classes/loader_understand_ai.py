# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from pathlib import Path

from ..._util._warning import _WarningsLogger
from ...format import understand_ai as uai_format
from ._loader_abc import LoaderABC
from .loader_raillabel import LoaderRailLabel


class LoaderUnderstandAi(LoaderABC):
    """Loader class for the Understand.Ai Trains4 annotation format.

    Attributes
    ----------
    scene: raillabel.format.understand_ai.Scene
        Loaded raillabel.format.understand_ai.Scene with the data.
    warnings: t.List[str]
        List of warning strings, that have been found during the execution of load().
    """

    scene: uai_format.Scene
    warnings: t.List[str]

    SCHEMA_PATH: Path = (
        Path(__file__).parent.parent.parent
        / "validate"
        / "schemas"
        / "understand_ai_t4_schema.json"
    )

    def load(self, data: dict, validate: bool = False) -> uai_format.Scene:
        """Load the data into a UAIScene and return it.

        Parameters
        ----------
        data: dict
            A dictionary loaded from a JSON-file.
        validate: bool
            If True, the annotation data is validated via the respective schema. This is highly
            recommended, as not validating the data may lead to Errors during loading or while
            handling the scene. However, validating may increase the loading time. Default is False.

        Returns
        -------
        scene: raillabel.format.understand_ai.UAIScene
            The loaded scene with the data.
        """

        if validate:
            self.validate(data)

        with _WarningsLogger() as logger:
            data_converted_to_raillabel = uai_format.Scene.fromdict(data).to_raillabel()

        raillabel_loader = LoaderRailLabel()
        raillabel_scene = raillabel_loader.load(data_converted_to_raillabel, validate=False)

        self.warnings = logger.warnings + raillabel_loader.warnings

        return raillabel_scene

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
            "metadata" in data
            and "project_id" in data["metadata"]
            and "coordinateSystems" in data
            and "frames" in data
        )
