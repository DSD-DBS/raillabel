# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Devkit for working with recorded and annotated train ride data from DB."""

from . import format, io
from .exceptions import *
from .format.scene import Scene
from .io.filter import filter
from .io.load import load
from .io.save import save
from .io.validate import validate

__version__ = "2.0.0"
