# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path

from raillabel.format import Scene


def save(scene: Scene, path: Path | str, prettify_json: bool = False) -> None:
    """Save a raillabel.Scene to a JSON file."""
    if prettify_json:
        json_data = scene.to_json().model_dump_json(exclude_none=True, indent=4)
    else:
        json_data = scene.to_json().model_dump_json(exclude_none=True)

    with Path(path).open("w") as scene_file:
        scene_file.write(json_data)
