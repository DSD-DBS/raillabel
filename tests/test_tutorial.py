# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from decimal import Decimal
from pathlib import Path

import pytest
import raillabel

# IMPORTANT!: These tests exist to ensure that the tutorial tasks actually work. If changes are
# introduced that break one of these tests, apply the necessary changes to the tutorial page as
# well.


@pytest.fixture
def path_to_calibration_json() -> Path:
    return Path(__file__).parent / "__test_assets__" / "1_calibration_1.1_labels.json"


def test_first_frame_id(path_to_calibration_json):
    scene = raillabel.load(path_to_calibration_json)
    frame_id_list = list(scene.frames.keys())
    first_frame_id = frame_id_list[0]

    assert first_frame_id == 12


def test_third_frame_timestamp(path_to_calibration_json):
    scene = raillabel.load(path_to_calibration_json)
    frame_id_list = list(scene.frames.keys())
    third_frame = scene.frames[frame_id_list[2]]
    third_frame_timestamp = third_frame.timestamp

    assert third_frame_timestamp == Decimal("1631441453.499971000")


def test_second_frame_annotation_number(path_to_calibration_json):
    scene = raillabel.load(path_to_calibration_json)
    frame_id_list = list(scene.frames.keys())
    second_frame = scene.frames[frame_id_list[2]]
    second_frame_annotation_number = len(second_frame.annotations)

    assert second_frame_annotation_number == 210


def test_number_of_cuboid_annotations_in_fourth_frame(path_to_calibration_json):
    scene = raillabel.load(path_to_calibration_json)

    # option 1:
    frame_id_list = list(scene.frames.keys())
    fourth_frame = scene.frames[frame_id_list[3]]
    number_of_cuboid_annotations_in_fourth_frame = 0
    for annotation in fourth_frame.annotations.values():
        if isinstance(annotation, raillabel.format.Cuboid):
            number_of_cuboid_annotations_in_fourth_frame += 1

    assert number_of_cuboid_annotations_in_fourth_frame == 15

    # option 2:
    filtered_scene = scene.filter(
        [
            raillabel.filter.IncludeFrameIdFilter([15]),
            raillabel.filter.IncludeAnnotationTypeFilter(["cuboid"]),
        ]
    )
    number_of_cuboid_annotations_in_fourth_frame = len(filtered_scene.annotations_with_frame_id())
    assert number_of_cuboid_annotations_in_fourth_frame == 15


def test_number_of_camera_sensors(path_to_calibration_json):
    scene = raillabel.load(path_to_calibration_json)

    # option 1:
    number_of_camera_sensors = 0
    for sensor in scene.sensors.values():
        if isinstance(sensor, raillabel.format.Camera):
            number_of_camera_sensors += 1

    assert number_of_camera_sensors == 9

    # option 2:
    filtered_scene = scene.filter([raillabel.filter.IncludeSensorTypeFilter(["camera"])])
    number_of_camera_sensors = len(filtered_scene.sensors)

    assert number_of_camera_sensors == 9


def test_number_of_objects(path_to_calibration_json):
    scene = raillabel.load(path_to_calibration_json)

    number_of_objects = len(scene.objects)

    assert number_of_objects == 37


def test_number_of_persons(path_to_calibration_json):
    scene = raillabel.load(path_to_calibration_json)

    # option 1:
    number_of_persons = 0
    for obj in scene.objects.values():
        if obj.type == "person":
            number_of_persons += 1

    assert number_of_persons == 3

    # option 2:
    filtered_scene = scene.filter([raillabel.filter.IncludeObjectTypeFilter(["person"])])
    number_of_persons = len(filtered_scene.objects)

    assert number_of_persons == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
