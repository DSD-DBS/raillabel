# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Devkit for working with recorded and annotated train ride data from DB."""

from importlib import metadata

from . import filter, format
from .format import Scene
from .load.load import load
from .save.save import save

__all__ = [
    "filter",
    "format",
    "Scene",
    "load",
    "save",
]

try:
    __version__ = metadata.version("raillabel")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0+unknown"
del metadata
