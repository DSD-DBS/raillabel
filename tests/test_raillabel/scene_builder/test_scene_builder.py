# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

import raillabel
from raillabel.format import Scene, Metadata
from raillabel.scene_builder.scene_builder import SceneBuilder


def test_empty():
    actual = SceneBuilder.empty()
    assert actual.scene == Scene(Metadata(schema_version="1.0.0"))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
