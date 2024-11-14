# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
from pathlib import Path

from raillabel.format import Scene
from raillabel.json_format import JSONScene


def load(path: Path | str) -> Scene:
    """Load an annotation file as a scene."""
    with Path(path).open() as annotation_file:
        json_data = json.load(annotation_file)
    return Scene.from_json(JSONScene(**json_data))
