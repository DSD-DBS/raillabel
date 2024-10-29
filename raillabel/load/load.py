# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json

from ..format import Scene


def load(path: str, validate: bool = False, show_warnings: bool = True) -> Scene:
    """Load an annotation file of any supported type.

    Parameters
    ----------
    path: str
        Path to the annotation file.

    Returns
    -------
    scene: raillabel.Scene
        Scene with the loaded data.
    """
    with path.open() as scene_file:
        raw_scene = json.load(scene_file)

    return Scene.fromdict(raw_scene)
