# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from uuid import UUID
from decimal import Decimal

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
    Frame,
    Bbox,
    Point2d,
    Size2d,
    Cuboid,
    Point3d,
    Size3d,
    Quaternion,
    Poly2d,
    Poly3d,
    Seg3d,
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


def test_add_sensor__camera_rgb(camera_empty):
    actual = SceneBuilder.empty().add_sensor("rgb_middle")
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        sensors={"rgb_middle": camera_empty},
    )


def test_add_sensor__camera_ir(camera_empty):
    actual = SceneBuilder.empty().add_sensor("ir_left")
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        sensors={"ir_left": camera_empty},
    )


def test_add_sensor__radar(radar_empty):
    actual = SceneBuilder.empty().add_sensor("radar")
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        sensors={"radar": radar_empty},
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


def test_add_frame():
    actual = SceneBuilder.empty().add_frame(1, 1631691173)
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"), frames={1: Frame(timestamp=Decimal(1631691173))}
    )


def test_add_frame__no_timestamp():
    actual = SceneBuilder.empty().add_frame(1)
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"), frames={1: Frame(timestamp=None)}
    )


def test_add_frame__no_frame_id():
    actual = SceneBuilder.empty().add_frame().add_frame()
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        frames={
            1: Frame(),
            2: Frame(),
        },
    )


def test_add_bbox(camera_empty):
    actual = SceneBuilder.empty().add_bbox(
        uid=UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"),
        frame_id=2,
        object_name="person_0001",
        sensor_id="ir_middle",
        attributes={"attr": True},
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"ir_middle": camera_empty},
        frames={
            2: Frame(
                annotations={
                    UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"): Bbox(
                        sensor_id="ir_middle",
                        object_id=UUID("5c59aad4-0000-4000-0000-000000000000"),
                        pos=Point2d(0, 0),
                        size=Size2d(0, 0),
                        attributes={"attr": True},
                    )
                }
            ),
        },
    )


def test_add_bbox__just_defaults(camera_empty):
    actual = SceneBuilder.empty().add_bbox()
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"rgb_middle": camera_empty},
        frames={
            1: Frame(
                annotations={
                    UUID("6c95543d-0000-4000-0000-000000000000"): Bbox(
                        sensor_id="rgb_middle",
                        object_id=UUID("5c59aad4-0000-4000-0000-000000000000"),
                        pos=Point2d(0, 0),
                        size=Size2d(0, 0),
                        attributes={},
                    )
                }
            ),
        },
    )


def test_add_cuboid():
    actual = SceneBuilder.empty().add_cuboid(
        uid=UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"),
        frame_id=2,
        object_name="person_0001",
        sensor_id="lidar_left",
        attributes={"my_attr": 5},
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"lidar_left": Lidar()},
        frames={
            2: Frame(
                annotations={
                    UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"): Cuboid(
                        sensor_id="lidar_left",
                        object_id=UUID("5c59aad4-0000-4000-0000-000000000000"),
                        pos=Point3d(0, 0, 0),
                        size=Size3d(0, 0, 0),
                        quat=Quaternion(0, 0, 0, 0),
                        attributes={"my_attr": 5},
                    )
                }
            ),
        },
    )


def test_add_cuboid__just_defaults():
    actual = SceneBuilder.empty().add_cuboid()
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"lidar": Lidar()},
        frames={
            1: Frame(
                annotations={
                    UUID("6c95543d-0000-4000-0000-000000000000"): Cuboid(
                        sensor_id="lidar",
                        object_id=UUID("5c59aad4-0000-4000-0000-000000000000"),
                        pos=Point3d(0, 0, 0),
                        size=Size3d(0, 0, 0),
                        quat=Quaternion(0, 0, 0, 0),
                        attributes={},
                    )
                }
            ),
        },
    )


def test_add_poly2d(camera_empty):
    actual = SceneBuilder.empty().add_poly2d(
        uid=UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"),
        frame_id=2,
        object_name="person_0001",
        sensor_id="ir_left",
        attributes={"my_attr": 5},
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"ir_left": camera_empty},
        frames={
            2: Frame(
                annotations={
                    UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"): Poly2d(
                        sensor_id="ir_left",
                        object_id=UUID("5c59aad4-0000-4000-0000-000000000000"),
                        points=[],
                        closed=False,
                        attributes={"my_attr": 5},
                    )
                }
            ),
        },
    )


def test_add_poly2d__just_defaults(camera_empty):
    actual = SceneBuilder.empty().add_poly2d()
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"rgb_middle": camera_empty},
        frames={
            1: Frame(
                annotations={
                    UUID("6c95543d-0000-4000-0000-000000000000"): Poly2d(
                        sensor_id="rgb_middle",
                        object_id=UUID("5c59aad4-0000-4000-0000-000000000000"),
                        points=[],
                        closed=False,
                        attributes={},
                    )
                }
            ),
        },
    )


def test_add_poly3d():
    actual = SceneBuilder.empty().add_poly3d(
        uid=UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"),
        frame_id=2,
        object_name="person_0001",
        sensor_id="lidar_right",
        attributes={"my_attr": 5},
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"lidar_right": Lidar()},
        frames={
            2: Frame(
                annotations={
                    UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"): Poly3d(
                        sensor_id="lidar_right",
                        object_id=UUID("5c59aad4-0000-4000-0000-000000000000"),
                        points=[],
                        closed=False,
                        attributes={"my_attr": 5},
                    )
                }
            ),
        },
    )


def test_add_poly3d__just_defaults():
    actual = SceneBuilder.empty().add_poly3d()
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"lidar": Lidar()},
        frames={
            1: Frame(
                annotations={
                    UUID("6c95543d-0000-4000-0000-000000000000"): Poly3d(
                        sensor_id="lidar",
                        object_id=UUID("5c59aad4-0000-4000-0000-000000000000"),
                        points=[],
                        closed=False,
                        attributes={},
                    )
                }
            ),
        },
    )


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
