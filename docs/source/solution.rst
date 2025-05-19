..
   Copyright DB InfraGO AG and contributors
   SPDX-License-Identifier: Apache-2.0

Solution
--------

This page contains the solutions to the tutorial exercises found :doc:`here <tutorial>`.

.. code-block:: python

    import raillabel

    path_to_calibration_json = ... # insert path to the downloaded 1_calibration_1.1_labels.json
    scene = raillabel.load(path_to_calibration_json)


    # Task 1: What is the ID of the first frame in the scene?
    frame_id_list = list(scene.frames.keys())
    first_frame_id = frame_id_list[0]

    assert first_frame_id == 12


    # Task 2: What is the timestamp of the third frame in the scene?
    frame_id_list = list(scene.frames.keys())
    third_frame = scene.frames[frame_id_list[2]]
    third_frame_timestamp = third_frame.timestamp

    assert third_frame_timestamp == Decimal("1631441453.499971000")


    # Task 3: How many annotations are in the second frame?
    frame_id_list = list(scene.frames.keys())
    second_frame = scene.frames[frame_id_list[2]]
    second_frame_annotation_number = len(second_frame.annotations)

    assert second_frame_annotation_number == 210


    # Task 4: How many cuboid annotations are in the fourth frame?

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


    # Task 5: How many camera sensors are in the scene?

    # option 1:
    number_of_camera_sensors = 0
    for sensor in scene.sensors.values():
        if isinstance(sensor, raillabel.format.Camera):
            number_of_camera_sensors += 1

    assert number_of_camera_sensors == 9

    # option 2:
    filtered_scene = scene.filter(
        [raillabel.filter.IncludeSensorTypeFilter(["camera"])]
    )
    number_of_camera_sensors = len(filtered_scene.sensors)

    assert number_of_camera_sensors == 9


    # Task 6: How many unique persons are in the scene?

    # option 1:
    number_of_persons = 0
    for obj in scene.objects.values():
        if obj.type == "person":
            number_of_persons += 1

    assert number_of_persons == 3

    # option 2:
    filtered_scene = scene.filter(
        [raillabel.filter.IncludeObjectTypeFilter(["person"])]
    )
    number_of_persons = len(filtered_scene.objects)

    assert number_of_persons == 3
