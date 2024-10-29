# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Frame, FrameInterval, Scene
from raillabel.format.scene import _clean_dict

# == Fixtures =========================


@pytest.fixture
def scene_dict(
    metadata_full_dict,
    sensor_camera_dict,
    sensor_lidar_dict,
    sensor_radar_dict,
    object_person_dict,
    object_train_dict,
    frame,
    frame_dict,
) -> dict:
    return {
        "openlabel": {
            "metadata": metadata_full_dict,
            "streams": {
                sensor_camera_dict["uid"]: sensor_camera_dict["stream"],
                sensor_lidar_dict["uid"]: sensor_lidar_dict["stream"],
                sensor_radar_dict["uid"]: sensor_radar_dict["stream"],
            },
            "coordinate_systems": {
                "base": {
                    "type": "local",
                    "parent": "",
                    "children": [
                        sensor_lidar_dict["uid"],
                        sensor_camera_dict["uid"],
                        sensor_radar_dict["uid"],
                    ],
                },
                sensor_camera_dict["uid"]: sensor_camera_dict["coordinate_system"],
                sensor_lidar_dict["uid"]: sensor_lidar_dict["coordinate_system"],
                sensor_radar_dict["uid"]: sensor_radar_dict["coordinate_system"],
            },
            "objects": {
                object_person_dict["object_uid"]: object_person_dict["data_dict"],
                object_train_dict["object_uid"]: object_train_dict["data_dict"],
            },
            "frames": {
                frame.uid: frame_dict,
            },
            "frame_intervals": [
                {
                    "frame_start": 0,
                    "frame_end": 0,
                }
            ],
        }
    }


@pytest.fixture
def scene(
    metadata_full, sensor_camera, sensor_lidar, sensor_radar, object_person, object_train, frame
) -> Scene:
    return Scene(
        metadata=metadata_full,
        sensors={
            sensor_lidar.uid: sensor_lidar,
            sensor_camera.uid: sensor_camera,
            sensor_radar.uid: sensor_radar,
        },
        objects={
            object_person.uid: object_person,
            object_train.uid: object_train,
        },
        frames={frame.uid: frame},
    )


# == Tests ============================


def test_fromdict_metadata(
    metadata_full,
    metadata_full_dict,
):
    scene = Scene.fromdict(
        {
            "openlabel": {
                "metadata": metadata_full_dict,
            }
        },
        subschema_version=metadata_full.subschema_version,
    )

    scene.metadata.exporter_version = None  # necessary for testing on remote

    assert scene.metadata == metadata_full


def test_fromdict_sensors(
    metadata_full_dict,
    sensor_camera,
    sensor_lidar,
    sensor_radar,
    sensor_camera_dict,
    sensor_lidar_dict,
    sensor_radar_dict,
):
    scene = Scene.fromdict(
        {
            "openlabel": {
                "metadata": metadata_full_dict,
                "streams": {
                    sensor_camera_dict["uid"]: sensor_camera_dict["stream"],
                    sensor_lidar_dict["uid"]: sensor_lidar_dict["stream"],
                    sensor_radar_dict["uid"]: sensor_radar_dict["stream"],
                },
                "coordinate_systems": {
                    "base": {
                        "type": "local",
                        "parent": "",
                        "children": [
                            sensor_lidar_dict["uid"],
                            sensor_camera_dict["uid"],
                            sensor_radar_dict["uid"],
                        ],
                    },
                    sensor_camera_dict["uid"]: sensor_camera_dict["coordinate_system"],
                    sensor_lidar_dict["uid"]: sensor_lidar_dict["coordinate_system"],
                    sensor_radar_dict["uid"]: sensor_radar_dict["coordinate_system"],
                },
            }
        }
    )

    assert scene.sensors == {
        sensor_lidar.uid: sensor_lidar,
        sensor_camera.uid: sensor_camera,
        sensor_radar.uid: sensor_radar,
    }


def test_fromdict_objects(
    metadata_full,
    metadata_full_dict,
    object_person,
    object_train,
    object_person_dict,
    object_train_dict,
):
    scene = Scene.fromdict(
        {
            "openlabel": {
                "metadata": metadata_full_dict,
                "objects": {
                    object_person_dict["object_uid"]: object_person_dict["data_dict"],
                    object_train_dict["object_uid"]: object_train_dict["data_dict"],
                },
            }
        },
        subschema_version=metadata_full.subschema_version,
    )

    assert scene.objects == {
        object_person.uid: object_person,
        object_train.uid: object_train,
    }


def test_fromdict_frames(
    metadata_full,
    metadata_full_dict,
    streams_dict,
    coordinate_systems_dict,
    objects_dict,
    frame,
    frame_dict,
):
    scene = Scene.fromdict(
        {
            "openlabel": {
                "metadata": metadata_full_dict,
                "streams": streams_dict,
                "coordinate_systems": coordinate_systems_dict,
                "objects": objects_dict,
                "frames": {
                    str(frame.uid): frame_dict,
                },
                "frame_intervals": [
                    {
                        "frame_start": 0,
                        "frame_end": 0,
                    }
                ],
            }
        },
        subschema_version=metadata_full.subschema_version,
    )

    assert scene.frames == {
        frame.uid: frame,
    }


def test_asdict_sensors(
    metadata_full,
    metadata_full_dict,
    sensor_camera,
    sensor_lidar,
    sensor_radar,
    sensor_camera_dict,
    sensor_lidar_dict,
    sensor_radar_dict,
):
    scene = Scene(
        metadata=metadata_full,
        sensors={
            sensor_lidar.uid: sensor_lidar,
            sensor_camera.uid: sensor_camera,
            sensor_radar.uid: sensor_radar,
        },
    )

    assert scene.asdict() == {
        "openlabel": {
            "metadata": metadata_full_dict,
            "streams": {
                sensor_camera_dict["uid"]: sensor_camera_dict["stream"],
                sensor_lidar_dict["uid"]: sensor_lidar_dict["stream"],
                sensor_radar_dict["uid"]: sensor_radar_dict["stream"],
            },
            "coordinate_systems": {
                "base": {
                    "type": "local",
                    "parent": "",
                    "children": [
                        sensor_lidar_dict["uid"],
                        sensor_camera_dict["uid"],
                        sensor_radar_dict["uid"],
                    ],
                },
                sensor_camera_dict["uid"]: sensor_camera_dict["coordinate_system"],
                sensor_lidar_dict["uid"]: sensor_lidar_dict["coordinate_system"],
                sensor_radar_dict["uid"]: sensor_radar_dict["coordinate_system"],
            },
        }
    }


def test_asdict_objects(
    metadata_full,
    metadata_full_dict,
    object_person,
    object_train,
    object_person_dict,
    object_train_dict,
):
    scene = Scene(
        metadata=metadata_full,
        objects={
            object_person.uid: object_person,
            object_train.uid: object_train,
        },
    )

    assert scene.asdict(calculate_pointers=False) == {
        "openlabel": {
            "metadata": metadata_full_dict,
            "objects": {
                object_person_dict["object_uid"]: object_person_dict["data_dict"],
                object_train_dict["object_uid"]: object_train_dict["data_dict"],
            },
        }
    }


def test_asdict_frames(
    metadata_full,
    metadata_full_dict,
    sensors,
    streams_dict,
    coordinate_systems_dict,
    objects,
    objects_dict,
    frame,
    frame_dict,
):
    scene = Scene(
        metadata=metadata_full,
        sensors=sensors,
        objects=objects,
        frames={
            frame.uid: frame,
        },
    )

    assert scene.asdict(calculate_pointers=False) == {
        "openlabel": {
            "metadata": metadata_full_dict,
            "streams": streams_dict,
            "coordinate_systems": coordinate_systems_dict,
            "objects": objects_dict,
            "frames": {
                str(frame.uid): frame_dict,
            },
            "frame_intervals": [
                {
                    "frame_start": 0,
                    "frame_end": 0,
                }
            ],
        }
    }


def test_frame_intervals(metadata_minimal):
    scene = Scene(
        metadata=metadata_minimal,
        frames={
            1: Frame(1),
            2: Frame(2),
            3: Frame(3),
            8: Frame(8),
        },
    )

    assert scene.frame_intervals == [
        FrameInterval(1, 3),
        FrameInterval(8, 8),
    ]


def test_integration(json_data):
    scene_dict = json_data["openlabel_v1_short"]

    actual = Scene.fromdict(scene_dict).asdict()

    del actual["openlabel"]["metadata"]["exporter_version"]
    assert actual == scene_dict


def test_clean_dict():
    input_dict = {"non_empty_field": "non_empty_value", "none_field": None, "field_with_len_0": []}

    assert _clean_dict(input_dict) == {
        "non_empty_field": "non_empty_value",
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-vv"])
