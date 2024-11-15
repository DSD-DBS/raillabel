# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from raillabel.format import Metadata, Scene


@dataclass
class SceneBuilder:
    """Use this class for easily creating scenes for tests."""

    scene: Scene

    @classmethod
    def empty(cls) -> SceneBuilder:
        """Construct the SceneBuilder with an empty scene."""
        return SceneBuilder(Scene(metadata=Metadata(schema_version="1.0.0")))
