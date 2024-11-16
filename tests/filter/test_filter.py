# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

import raillabel
from raillabel.scene_builder import SceneBuilder


def test_include_frames():
    scene = SceneBuilder.empty().add_frame(1).add_frame(2).add_frame(3).result
    filters = [raillabel.filter.IncludeFrameIdFilter([1, 3])]

    actual = raillabel.filter.filter_(scene, filters)
    assert actual == SceneBuilder.empty().add_frame(1).add_frame(3).result


def test_exclude_frames():
    scene = SceneBuilder.empty().add_frame(1).add_frame(2).add_frame(3).result
    filters = [raillabel.filter.ExcludeFrameIdFilter([2])]

    actual = raillabel.filter.filter_(scene, filters)
    assert actual == SceneBuilder.empty().add_frame(1).add_frame(3).result


def test_start_time():
    scene = SceneBuilder.empty().add_frame(1, 100).add_frame(2, 200).add_frame(3, 300).result
    filters = [raillabel.filter.StartTimeFilter(150)]

    actual = raillabel.filter.filter_(scene, filters)
    assert actual == SceneBuilder.empty().add_frame(2, 200).add_frame(3, 300).result


def test_start_time():
    scene = SceneBuilder.empty().add_frame(1, 100).add_frame(2, 200).add_frame(3, 300).result
    filters = [raillabel.filter.EndTimeFilter(250)]

    actual = raillabel.filter.filter_(scene, filters)
    assert actual == SceneBuilder.empty().add_frame(1, 100).add_frame(2, 200).result


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
