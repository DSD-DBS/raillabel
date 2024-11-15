# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from uuid import UUID

import pytest

import raillabel
from raillabel.scene_builder.scene_builder import SceneBuilder
from raillabel.format import (
    Scene,
    Metadata,
    Object,
    Camera,
    Lidar,
    Radar,
    GpsImu,
    OtherSensor,
    IntrinsicsPinhole,
    IntrinsicsRadar,
)


def test_empty():
    actual = SceneBuilder.empty()
    assert actual.result == Scene(Metadata(schema_version="1.0.0"))


def test_add_object__all_options():
    actual = SceneBuilder.empty().add_object(
        object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
        object_type="train",
        object_name="train_0001",
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="train_0001", type="train")
        },
    )


def test_add_object__no_object_name():
    actual = SceneBuilder.empty().add_object(
        object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
        object_type="train",
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="train_0000", type="train")
        },
    )


def test_add_object__no_object_type():
    actual = SceneBuilder.empty().add_object(
        object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
        object_name="train_0000",
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="train_0000", type="train")
        },
    )


def test_add_object__no_object_type_or_name():
    actual = SceneBuilder.empty().add_object(
        object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="person_0000", type="person")
        },
    )


def test_add_object__no_object_id():
    actual = SceneBuilder.empty().add_object(object_type="train", object_name="train_0001")
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="train_0001", type="train")
        },
    )


def test_add_object__object_id_iteration():
    actual = SceneBuilder.empty().add_object().add_object().add_object().add_object()
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0000", type="person"),
            UUID("5c59aad4-0000-4000-0000-000000000001"): Object(name="person_0000", type="person"),
            UUID("5c59aad4-0000-4000-0000-000000000002"): Object(name="person_0000", type="person"),
            UUID("5c59aad4-0000-4000-0000-000000000003"): Object(name="person_0000", type="person"),
        },
    )


def test_add_sensor__camera_rgb():
    actual = SceneBuilder.empty().add_sensor("rgb_middle")
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        sensors={
            "rgb_middle": Camera(
                intrinsics=IntrinsicsPinhole(
                    camera_matrix=tuple([0] * 12),
                    distortion=tuple([0] * 5),
                    width_px=0,
                    height_px=0,
                )
            )
        },
    )


def test_add_sensor__camera_ir():
    actual = SceneBuilder.empty().add_sensor("ir_left")
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        sensors={
            "ir_left": Camera(
                intrinsics=IntrinsicsPinhole(
                    camera_matrix=tuple([0] * 12),
                    distortion=tuple([0] * 5),
                    width_px=0,
                    height_px=0,
                )
            )
        },
    )


def test_add_sensor__radar():
    actual = SceneBuilder.empty().add_sensor("radar")
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        sensors={
            "radar": Radar(
                intrinsics=IntrinsicsRadar(
                    resolution_px_per_m=0,
                    width_px=0,
                    height_px=0,
                )
            )
        },
    )


def test_add_sensor__lidar():
    actual = SceneBuilder.empty().add_sensor("lidar")
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"), sensors={"lidar": Lidar()}
    )


def test_add_sensor__gps_imu():
    actual = SceneBuilder.empty().add_sensor("gps_imu")
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"), sensors={"gps_imu": GpsImu()}
    )


def test_add_sensor__other():
    actual = SceneBuilder.empty().add_sensor("SOMETHING_ELSE")
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"), sensors={"SOMETHING_ELSE": OtherSensor()}
    )


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
