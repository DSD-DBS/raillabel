# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
from pathlib import Path

from . import exceptions
from .format import Scene
from .validate import validate as validate_func


def save(scene: Scene, path: str, prettify_json: bool = False, validate: bool = False):
    """Save a raillabel.Scene in a JSON file.

    Parameters
    ----------
    scene: raillabel.Scene
        Scene, which should be saved.
    path: str
        Path to the file location, that should be used for saving.
    save_path: str
        Path to the JSON file.
    prettify_json: bool, optional
        If true, the JSON is saved with linebreaks and indents. This increases readibility but
        also the file size. Default is False.
    validate: bool, optional
        If True, the annotation data is validated via the OpenLabel schema. This is highly
        recommended, as not validating the data may lead to Errors during loading or while handling
        the scene. However, validating may increase the loading time. Default is False.

    Raises
    ------
    SchemaError
        If the data does not validate via the OpenLabel schema.
    FileNotFoundError
        If the save_path does not point to an accessible file.
    """

    path = Path(path)

    # Converts the data stored in the scene into a dictionary
    data = scene.asdict()

    # Validates the data
    if validate:
        is_data_valid, err_msgs = validate_func(data)
        if not is_data_valid:
            schema_err_msg = (
                "The data could not be saved, because it does not validate "
                "against the OpenLabel schema:"
            )

            for err_msg in err_msgs:
                schema_err_msg += "\n - " + err_msg

            raise exceptions.SchemaError(schema_err_msg)

    # Saves the data
    with path.open("w") as save_file:

        if prettify_json:
            json.dump(data, save_file, indent=4)
        else:
            json.dump(data, save_file)
