# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Devkit for working with recorded and annotated train ride data from DB.

The first step in using raillabel is downloading a desired dataset
(like [OSDaR23](https://data.fid-move.de/dataset/osdar23)). You can then load any scene by running

.. code-block:: python

    import raillabel

    scene = raillabel.load("path/to/annotation_file.json")

This returns the root class for the annotations.

If a file is too extensive for your use-case you can filter out certain parts of a scene like this

.. code-block:: python

    from raillabel.filter import (
        IncludeObjectTypeFilter,
        ExcludeAnnotationTypeFilter,
        StartTimeFilter, ExcludeFrameIdFilter,
        IncludeAttributesFilter
    )

    scene_with_only_trains = scene.filter([IncludeObjectTypeFilter(["rail_vehicle"])])

    scene_without_bboxs = scene.filter([ExcludeAnnotationTypeFilter(["bbox"])])

    cut_scene_with_only_red_trains = scene.filter([
        StartTimeFilter("1587349200.004200000"),
        ExcludeFrameIdFilter([2, 4]),
        IncludeObjectTypeFilter(["rail_vehicle"]),
        IncludeAttributesFilter({"color": "red"}),
    ])

An overview of all available filters can be found [here](https://dsd-dbs.github.io/raillabel/code/raillabel.filter.html#module-raillabel.filter).

If you then want to save your changes, then use

.. code-block:: python

    raillabel.save(cut_scene_with_only_red_trains, "/path/to/target.json")
"""

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
