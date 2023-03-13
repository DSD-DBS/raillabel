# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Devkit for working with recorded and annotated train ride data from DB."""
from importlib import metadata

from . import format
from .exceptions import *
from .filter import filter
from .format.scene import Scene
from .load import load
from .save import save
from .validate import validate

try:
    __version__ = metadata.version("pyraillabel")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0+unknown"
del metadata
