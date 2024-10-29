# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
from pathlib import Path

from raillabel.format import Scene


def load(path: Path | str) -> Scene:
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
    with Path(path).open() as scene_file:
        raw_scene = json.load(scene_file)

    return Scene.fromdict(raw_scene)
