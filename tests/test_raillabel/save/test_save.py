# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

import raillabel
from raillabel import Scene
from raillabel.json_format import JSONScene


def test_save(json_data, tmp_path):
    scene_path = tmp_path / "scene.json"
    ground_truth_scene = Scene.from_json(JSONScene(**json_data["openlabel_v1_short"]))
    raillabel.save(ground_truth_scene, scene_path)

    actual = raillabel.load(scene_path)
    assert actual == ground_truth_scene


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
