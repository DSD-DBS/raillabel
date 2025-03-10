# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from uuid import UUID
from decimal import Decimal

import pytest

from raillabel.scene_builder.scene_builder import SceneBuilder
from raillabel.format import (
    Scene,
    Metadata,
    Object,
    Lidar,
    GpsImu,
    OtherSensor,
    Frame,
    Bbox,
    Point2d,
    SensorReference,
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
    actual = SceneBuilder.empty().result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(Metadata(schema_version="1.0.0"))


def test_add_object__all_options():
    actual = (
        SceneBuilder.empty()
        .add_object(
            object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
            object_type="train",
            object_name="train_0001",
        )
        .result
    )

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="train_0001", type="train")
        },
    )


def test_add_object__no_object_name():
    actual = (
        SceneBuilder.empty()
        .add_object(
            object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
            object_type="train",
        )
        .result
    )

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="train_0000", type="train")
        },
    )


def test_add_object__no_object_type():
    actual = (
        SceneBuilder.empty()
        .add_object(
            object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
            object_name="train_0000",
        )
        .result
    )

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="train_0000", type="train")
        },
    )


def test_add_object__no_object_type_or_name():
    actual = (
        SceneBuilder.empty()
        .add_object(
            object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
        )
        .result
    )

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="person_0000", type="person")
        },
    )


def test_add_object__no_object_id():
    actual = SceneBuilder.empty().add_object(object_type="train", object_name="train_0001").result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="train_0001", type="train")
        },
    )


def test_add_object__object_id_iteration():
    actual = SceneBuilder.empty().add_object().add_object().add_object().add_object().result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0000", type="person"),
            UUID("5c59aad4-0000-4000-0000-000000000001"): Object(name="person_0000", type="person"),
            UUID("5c59aad4-0000-4000-0000-000000000002"): Object(name="person_0000", type="person"),
            UUID("5c59aad4-0000-4000-0000-000000000003"): Object(name="person_0000", type="person"),
        },
    )


def test_add_sensor__camera_rgb(camera_empty):
    actual = SceneBuilder.empty().add_sensor("rgb_center").result

    actual.to_json()
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        sensors={"rgb_center": camera_empty},
    )


def test_add_sensor__camera_ir(camera_empty):
    actual = SceneBuilder.empty().add_sensor("ir_left").result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        sensors={"ir_left": camera_empty},
    )


def test_add_sensor__radar(radar_empty):
    actual = SceneBuilder.empty().add_sensor("radar").result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        sensors={"radar": radar_empty},
    )


def test_add_sensor__lidar():
    actual = SceneBuilder.empty().add_sensor("lidar").result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(metadata=Metadata(schema_version="1.0.0"), sensors={"lidar": Lidar()})


def test_add_sensor__gps_imu():
    actual = SceneBuilder.empty().add_sensor("gps_imu").result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(metadata=Metadata(schema_version="1.0.0"), sensors={"gps_imu": GpsImu()})


def test_add_sensor__other():
    actual = SceneBuilder.empty().add_sensor("SOMETHING_ELSE").result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"), sensors={"SOMETHING_ELSE": OtherSensor()}
    )


def test_add_frame():
    actual = SceneBuilder.empty().add_frame(1, 1631691173).result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"), frames={1: Frame(timestamp=Decimal(1631691173))}
    )


def test_add_frame__no_timestamp():
    actual = SceneBuilder.empty().add_frame(1).result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"), frames={1: Frame(timestamp=None)}
    )


def test_add_frame__no_frame_id():
    actual = SceneBuilder.empty().add_frame().add_frame().result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        frames={
            1: Frame(),
            2: Frame(),
        },
    )


def test_add_bbox(camera_empty):
    actual = (
        SceneBuilder.empty()
        .add_bbox(
            uid=UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"),
            pos=Point2d(1, 2),
            size=Size2d(3, 4),
            frame_id=2,
            object_name="person_0001",
            sensor_id="ir_center",
            attributes={"attr": True},
        )
        .result
    )

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"ir_center": camera_empty},
        frames={
            2: Frame(
                annotations={
                    UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"): Bbox(
                        sensor_id="ir_center",
                        object_id=UUID("5c59aad4-0000-4000-0000-000000000000"),
                        pos=Point2d(1, 2),
                        size=Size2d(3, 4),
                        attributes={"attr": True},
                    )
                }
            ),
        },
    )


def test_add_bbox__just_defaults(camera_empty):
    actual = SceneBuilder.empty().add_bbox().result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"rgb_center": camera_empty},
        frames={
            1: Frame(
                annotations={
                    UUID("6c95543d-0000-4000-0000-000000000000"): Bbox(
                        sensor_id="rgb_center",
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
    actual = (
        SceneBuilder.empty()
        .add_cuboid(
            uid=UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"),
            pos=Point3d(1, 2, 3),
            quat=Quaternion(4, 5, 6, 7),
            size=Size3d(8, 9, 10),
            frame_id=2,
            object_name="person_0001",
            sensor_id="lidar_left",
            attributes={"my_attr": 5},
        )
        .result
    )

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
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
                        pos=Point3d(1, 2, 3),
                        size=Size3d(8, 9, 10),
                        quat=Quaternion(4, 5, 6, 7),
                        attributes={"my_attr": 5},
                    )
                }
            ),
        },
    )


def test_add_cuboid__just_defaults():
    actual = SceneBuilder.empty().add_cuboid().result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
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
    actual = (
        SceneBuilder.empty()
        .add_poly2d(
            uid=UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"),
            points=[Point2d(0.0, 1.0), Point2d(2.0, 3.0)],
            frame_id=2,
            object_name="person_0001",
            sensor_id="ir_left",
            attributes={"my_attr": 5},
        )
        .result
    )

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
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
                        points=[Point2d(0.0, 1.0), Point2d(2.0, 3.0)],
                        closed=False,
                        attributes={"my_attr": 5},
                    )
                }
            ),
        },
    )


def test_add_poly2d__just_defaults(camera_empty):
    actual = SceneBuilder.empty().add_poly2d().result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"rgb_center": camera_empty},
        frames={
            1: Frame(
                annotations={
                    UUID("6c95543d-0000-4000-0000-000000000000"): Poly2d(
                        sensor_id="rgb_center",
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
    actual = (
        SceneBuilder.empty()
        .add_poly3d(
            uid=UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"),
            points=[Point3d(1, 2, 3), Point3d(4, 5, 6)],
            frame_id=2,
            object_name="person_0001",
            sensor_id="lidar_right",
            attributes={"my_attr": 5},
        )
        .result
    )

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
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
                        points=[Point3d(1, 2, 3), Point3d(4, 5, 6)],
                        closed=False,
                        attributes={"my_attr": 5},
                    )
                }
            ),
        },
    )


def test_add_poly3d__just_defaults():
    actual = SceneBuilder.empty().add_poly3d().result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
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


def test_add_seg3d():
    actual = (
        SceneBuilder.empty()
        .add_seg3d(
            uid=UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"),
            point_ids=[1, 2, 3],
            frame_id=2,
            object_name="person_0001",
            sensor_id="lidar_right",
            attributes={"my_attr": 5},
        )
        .result
    )

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"lidar_right": Lidar()},
        frames={
            2: Frame(
                annotations={
                    UUID("6c95543d-4d4f-43df-a52d-36bf868e09d8"): Seg3d(
                        sensor_id="lidar_right",
                        object_id=UUID("5c59aad4-0000-4000-0000-000000000000"),
                        point_ids=[1, 2, 3],
                        attributes={"my_attr": 5},
                    )
                }
            ),
        },
    )


def test_add_seg3d__just_defaults():
    actual = SceneBuilder.empty().add_seg3d().result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0001", type="person")
        },
        sensors={"lidar": Lidar()},
        frames={
            1: Frame(
                annotations={
                    UUID("6c95543d-0000-4000-0000-000000000000"): Seg3d(
                        sensor_id="lidar",
                        object_id=UUID("5c59aad4-0000-4000-0000-000000000000"),
                        point_ids=[],
                        attributes={},
                    )
                }
            ),
        },
    )


def test_add_annotation():
    bbox = Bbox(
        pos=Point2d(0, 0),
        size=Size2d(0, 0),
        object_id=UUID("ffffffff-ffff-4fff-ffff-ffffffffffff"),
        sensor_id="rgb_center",
        attributes={},
    )
    actual = SceneBuilder.empty().add_annotation(bbox).result

    actual.to_json()  # check if scene is also valid in JSON
    assert actual == SceneBuilder.empty().add_bbox().result


def test_result_has_no_frame_sensors_due_to_no_timestamp():
    actual = (
        SceneBuilder.empty()
        .add_sensor("rgb_center")
        .add_frame(timestamp=None)
        .add_frame(timestamp=None)
        .add_sensor("lidar")
        .result
    )

    actual.to_json()  # check if scene is also valid in JSON
    assert actual.frames == {
        1: Frame(
            timestamp=None,
            sensors={},
        ),
        2: Frame(
            timestamp=None,
            sensors={},
        ),
    }


def test_result_has_all_frame_sensors():
    actual = (
        SceneBuilder.empty()
        .add_sensor("rgb_center")
        .add_frame(timestamp=12345)
        .add_frame(timestamp=67890)
        .add_sensor("lidar")
        .result
    )

    actual.to_json()  # check if scene is also valid in JSON
    assert actual.frames == {
        1: Frame(
            timestamp=Decimal(12345),
            sensors={
                "rgb_center": SensorReference(timestamp=Decimal(12345)),
                "lidar": SensorReference(timestamp=Decimal(12345)),
            },
        ),
        2: Frame(
            timestamp=Decimal(67890),
            sensors={
                "rgb_center": SensorReference(timestamp=Decimal(67890)),
                "lidar": SensorReference(timestamp=Decimal(67890)),
            },
        ),
    }


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
