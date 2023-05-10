# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from pathlib import Path

from .. import format
from ._loader_abc import LoaderABC


class LoaderUnderstandAiT4(LoaderABC):
    """Loader class for the Understand.Ai Trains4 annotation format.

    Attributes
    ----------
    scene: raillabel._understand_ai_t4_format.Scene
        Loaded raillabel._understand_ai_t4_format.Scene with the data.
    warnings: t.List[str]
        List of warning strings, that have been found during the execution of load().
    """

    scene: format.Scene
    warnings: t.List[str]

    SCHEMA_PATH: Path = Path(__file__).parent.parent / "schemas" / "understand_ai_t4_schema.json"

    def load(self, data: dict, validate: bool = True) -> format.Scene:
        """Load the data into a UAIScene and return it.

        Parameters
        ----------
        data: dict
            A dictionary loaded from a JSON-file.
        validate: bool
            If True, the annotation data is validated via the respective schema. This is highly
            recommended, as not validating the data may lead to Errors during loading or while
            handling the scene. However, validating may increase the loading time. Default is True.

        Returns
        -------
        scene: raillabel._understand_ai_t4_format.UAIScene
            The loaded scene with the data.
        """
        raise NotImplementedError

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
            and data["metadata"]["project_id"] == "trains_4"
            and "coordinateSystems" in data
            and "frames" in data
        )
