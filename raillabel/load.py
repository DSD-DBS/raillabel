# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json

from . import exceptions, format, format_loaders
from .format_loaders._loader_abc import LoaderABC


def load(path: str, validate: bool = False, show_warnings: bool = True) -> format.Scene:
    """Load an annotation file of any supported type.

    Parameters
    ----------
    path: str
        Path to the annotation file.
    validate: bool, optional
        If True, the annotation data is validated via the respective schema. This is highly
        recommended, as not validating the data may lead to Errors during loading or while handling
        the scene. However, validating may increase the loading time. Default is False.
    show_warnings: bool, optional
        If True, any non-critical inconsistencies in the data are output as a warning. Default is
        True.

    Returns
    -------
    scene: raillabel.Scene
        Scene with the loaded data.

    Raises
    ------
    raillabel.exceptions.UnsupportedFormatError
        if the annotation file does not match any loaders.
    raillabel.exceptions.SchemaError
        if during the validation, errors in the annotation file are found.
    """

    # To expand the supported formats in a simple manner, load() automatically fetches all classes
    # in the format_loaders directory and checks if they are suitable as loaders. To avoid errors
    # caused by potential other files and classes in the directory, only classes, which inherite
    # from LoaderABC are considered.

    loader_classes = []
    for cls in format_loaders.__dict__.values():
        if isinstance(cls, type) and issubclass(cls, LoaderABC) and cls != LoaderABC:
            loader_classes.append(cls)

    # Checks for the supported file type
    if not str(path).lower().endswith(".json"):
        raise exceptions.UnsupportedFormatError(f"{path} is not in a supported file format.")

    # Loads the JSON data
    with open(path) as data_file:
        data = json.load(data_file)

    # Iterates over the loader classes to find a suitable one
    for loader_class in loader_classes:

        loader = loader_class()

        # Checks if the loader supports the data
        if not loader.supports(data):
            continue

        # Loads the scene
        scene = loader.load(data, validate=validate)

        # Outputs the warnings
        if show_warnings:

            if len(loader.warnings) > 0:
                print(f"During the loading of {path} warnings have occurred:")

                for warning in loader.warnings:
                    print(" - " + warning)

        return scene

    # This part of the code is only reached if no suitable loader has been found or the data is
    # not in a supported file format. Therefore an exception is raised.

    raise exceptions.UnsupportedFormatError(f"{path} is not in a supported file format.")
