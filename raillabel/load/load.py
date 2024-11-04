# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path

from raillabel.format import Metadata, Scene


def load(_path: Path | str) -> Scene:
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
    return Scene(metadata=Metadata("1.0.0"))
