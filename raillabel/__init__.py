# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Devkit for working with recorded and annotated train ride data from DB."""

from importlib import metadata

from . import format
from .exceptions import *
from .filter.filter import filter
from .format import Scene
from .load.load import load
from .save.save import save

try:
    __version__ = metadata.version("raillabel")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0+unknown"
del metadata
