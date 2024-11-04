# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path

from raillabel.format import Scene


def save(_scene: Scene, _path: Path | str, _prettify_json: bool = False) -> None:
    """Save a raillabel.Scene in a JSON file.

    Parameters
    ----------
    scene: raillabel.Scene
        Scene, which should be saved.
    path: str
        Path to the file location, that should be used for saving.
    save_path: str
        Path to the JSON file.
    prettify_json: bool, optional
        If true, the JSON is saved with linebreaks and indents. This increases readibility but
        also the file size. Default is False.

    """
