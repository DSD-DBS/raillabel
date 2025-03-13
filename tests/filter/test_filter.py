# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from uuid import UUID

import pytest

import raillabel
from raillabel.scene_builder import SceneBuilder


def test_include_frame_ids():
    scene = SceneBuilder.empty().add_frame(1).add_frame(2).add_frame(3).result
    filters = [raillabel.filter.IncludeFrameIdFilter([1, 3])]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_frame(1).add_frame(3).result


def test_exclude_frame_ids():
    scene = SceneBuilder.empty().add_frame(1).add_frame(2).add_frame(3).result
    filters = [raillabel.filter.ExcludeFrameIdFilter([2])]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_frame(1).add_frame(3).result


def test_start_time():
    scene = SceneBuilder.empty().add_frame(1, 100).add_frame(2, 200).add_frame(3, 300).result
    filters = [raillabel.filter.StartTimeFilter(150)]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_frame(2, 200).add_frame(3, 300).result


def test_end_time():
    scene = SceneBuilder.empty().add_frame(1, 100).add_frame(2, 200).add_frame(3, 300).result
    filters = [raillabel.filter.EndTimeFilter(250)]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_frame(1, 100).add_frame(2, 200).result


def test_include_annotation_ids():
    scene = (
        SceneBuilder.empty()
        .add_bbox(uid="6c95543d-0000-4000-0000-000000000000")
        .add_bbox(uid="6c95543d-0000-4000-0000-000000000001")
        .add_bbox(uid="6c95543d-0000-4000-0000-000000000002")
        .result
    )
    filters = [
        raillabel.filter.IncludeAnnotationIdFilter(
            [
                UUID("6c95543d-0000-4000-0000-000000000000"),
                UUID("6c95543d-0000-4000-0000-000000000002"),
            ]
        )
    ]

    actual = scene.filter(filters)
    assert (
        actual
        == SceneBuilder.empty()
        .add_bbox(uid="6c95543d-0000-4000-0000-000000000000")
        .add_bbox(uid="6c95543d-0000-4000-0000-000000000002")
        .result
    )


def test_exclude_annotation_ids():
    scene = (
        SceneBuilder.empty()
        .add_bbox(uid="6c95543d-0000-4000-0000-000000000000")
        .add_bbox(uid="6c95543d-0000-4000-0000-000000000001")
        .add_bbox(uid="6c95543d-0000-4000-0000-000000000002")
        .result
    )
    filters = [
        raillabel.filter.ExcludeAnnotationIdFilter([UUID("6c95543d-0000-4000-0000-000000000001")])
    ]

    actual = scene.filter(filters)
    assert (
        actual
        == SceneBuilder.empty()
        .add_bbox(uid="6c95543d-0000-4000-0000-000000000000")
        .add_bbox(uid="6c95543d-0000-4000-0000-000000000002")
        .result
    )


def test_include_annotation_type():
    scene = SceneBuilder.empty().add_bbox().add_cuboid().result
    filters = [raillabel.filter.IncludeAnnotationTypeFilter(["bbox"])]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox().result


def test_exclude_annotation_type():
    scene = SceneBuilder.empty().add_bbox().add_cuboid().result
    filters = [raillabel.filter.ExcludeAnnotationTypeFilter(["cuboid"])]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox().result


def test_include_object_ids():
    scene = (
        SceneBuilder.empty()
        .add_bbox(object_name="person_0001")
        .add_cuboid(object_name="train_0001")
        .result
    )
    filters = [
        raillabel.filter.IncludeObjectIdFilter([UUID("5c59aad4-0000-4000-0000-000000000000")])
    ]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(object_name="person_0001").result


def test_exclude_object_ids():
    scene = (
        SceneBuilder.empty()
        .add_bbox(object_name="person_0001")
        .add_cuboid(object_name="train_0001")
        .result
    )
    filters = [
        raillabel.filter.ExcludeObjectIdFilter([UUID("5c59aad4-0000-4000-0000-000000000001")])
    ]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(object_name="person_0001").result


def test_include_object_types():
    scene = (
        SceneBuilder.empty()
        .add_bbox(object_name="person_0001")
        .add_cuboid(object_name="train_0001")
        .result
    )
    filters = [raillabel.filter.IncludeObjectTypeFilter(["person"])]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(object_name="person_0001").result


def test_exclude_object_types():
    scene = (
        SceneBuilder.empty()
        .add_bbox(object_name="person_0001")
        .add_cuboid(object_name="train_0001")
        .result
    )
    filters = [raillabel.filter.ExcludeObjectTypeFilter(["train"])]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(object_name="person_0001").result


def test_include_sensor_ids():
    scene = (
        SceneBuilder.empty().add_bbox(sensor_id="rgb_center").add_cuboid(sensor_id="lidar").result
    )
    filters = [raillabel.filter.IncludeSensorIdFilter(["rgb_center"])]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(sensor_id="rgb_center").result


def test_exclude_sensor_ids():
    scene = (
        SceneBuilder.empty().add_bbox(sensor_id="rgb_center").add_cuboid(sensor_id="lidar").result
    )
    filters = [raillabel.filter.ExcludeSensorIdFilter(["lidar"])]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(sensor_id="rgb_center").result


def test_include_sensor_types():
    scene = (
        SceneBuilder.empty()
        .add_bbox(sensor_id="rgb_center")
        .add_cuboid(sensor_id="lidar_center")
        .result
    )
    filters = [raillabel.filter.IncludeSensorTypeFilter(["camera"])]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(sensor_id="rgb_center").result


def test_exclude_sensor_types():
    scene = (
        SceneBuilder.empty()
        .add_bbox(sensor_id="rgb_center")
        .add_cuboid(sensor_id="lidar_center")
        .result
    )
    filters = [raillabel.filter.ExcludeSensorTypeFilter(["lidar"])]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(sensor_id="rgb_center").result


def test_include_attributes__only_keys():
    scene = (
        SceneBuilder.empty()
        .add_bbox(attributes={"length": 42})
        .add_bbox(attributes={"width": 34})
        .result
    )
    filters = [raillabel.filter.IncludeAttributesFilter({"length": None})]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(attributes={"length": 42}).result


def test_include_attributes__with_values():
    scene = (
        SceneBuilder.empty()
        .add_bbox(attributes={"is_dummy": True})
        .add_bbox(attributes={"is_dummy": False})
        .result
    )
    filters = [raillabel.filter.IncludeAttributesFilter({"is_dummy": True})]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(attributes={"is_dummy": True}).result


def test_exclude_attributes__only_keys():
    scene = (
        SceneBuilder.empty()
        .add_bbox(attributes={"length": 42})
        .add_bbox(attributes={"width": 34})
        .result
    )
    filters = [raillabel.filter.ExcludeAttributesFilter({"width": None})]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(attributes={"length": 42}).result


def test_exclude_attributes__with_values():
    scene = (
        SceneBuilder.empty()
        .add_bbox(attributes={"is_dummy": True})
        .add_bbox(attributes={"is_dummy": False})
        .result
    )
    filters = [raillabel.filter.ExcludeAttributesFilter({"is_dummy": False})]

    actual = scene.filter(filters)
    assert actual == SceneBuilder.empty().add_bbox(attributes={"is_dummy": True}).result


def test_remove_unused_sensors():
    scene = (
        SceneBuilder.empty().add_bbox(sensor_id="rgb_center").add_cuboid(sensor_id="lidar").result
    )
    filters = [raillabel.filter.ExcludeSensorIdFilter(["lidar"])]

    actual = scene.filter(filters)
    assert "rgb_center" in actual.sensors
    assert "lidar" not in actual.sensors


def test_remove_unused_sensor_references():
    scene = (
        SceneBuilder.empty()
        .add_frame(frame_id=1, timestamp=1234)
        .add_bbox(frame_id=1, sensor_id="rgb_center")
        .add_cuboid(frame_id=1, sensor_id="lidar")
        .result
    )
    filters = [raillabel.filter.ExcludeSensorIdFilter(["lidar"])]

    actual = scene.filter(filters)
    assert "rgb_center" in actual.frames[1].sensors
    assert "lidar" not in actual.frames[1].sensors


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
