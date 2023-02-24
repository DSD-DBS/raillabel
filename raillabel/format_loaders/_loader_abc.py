# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from abc import ABC, abstractmethod
from pathlib import Path

from .. import format
from ..exceptions import SchemaError
from ..validate import validate as global_validate


class LoaderABC(ABC):
    """Abstract base class of the annotation file loaders.

    For every annotation format, that can be loaded via raillabel, a loader class should exists,
    that inherites from this class.

    Attributes
    ----------
    scene: raillabel.Scene
        Loaded raillabel.Scene with the data.
    warnings: list[str]
        List of warning strings, that have been found during the execution of load().
    SCHEMA_PATH: Path
        Absolute path to the JSON schema.
    """

    scene: format.Scene
    warnings: t.List[str]
    SCHEMA_PATH: Path

    @abstractmethod
    def load(self, data: dict, validate: bool = True) -> format.Scene:
        """Load JSON-data into a raillabel.Scene.

        Any non-critical errors are stored in the warnings-property.

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
        scene: raillabel.Scene
            The loaded scene with the data.

        Raises
        ------
        raillabel.exceptions.SchemaError
            if validate is True and the data does not validate against the schema.
        """
        raise NotImplementedError

    @abstractmethod
    def supports(self, data: dict) -> bool:
        """Determine if the loader class is suitable for the data.

        This is performed based on hints in the data structure and can therefore be done
        efficiently.

        Parameters
        ----------
        data: dict
            A dictionary loaded from a JSON-file.

        Returns
        -------
        bool:
            If True, the Loader class is suitable for the data.
        """
        raise NotImplementedError

    def validate(self, data: dict) -> t.Tuple[bool, t.List[str]]:
        """Validate JSON-data with the corresponding schema.

        Parameters
        ----------
        data: dict
            JSON data to be validated.

        Raises
        ------
        raillabel.exceptions.SchemaError
            if the schema is not valid.
        """

        is_data_valid, schema_errors = global_validate(data, str(self.SCHEMA_PATH))
        if not is_data_valid:

            error_msg = (
                "The loaded data does not validate against the schema. Errors in the schema:\n"
            )

            for err in schema_errors:
                error_msg += " - " + err + "\n"

            raise SchemaError(error_msg)
