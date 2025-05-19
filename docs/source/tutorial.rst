..
   Copyright DB InfraGO AG and contributors
   SPDX-License-Identifier: Apache-2.0

Tutorial
--------

This page contains some tutorial tasks that you can solve to geet a better understanding of raillabel and its concepts. Every task is based on the `1_calibration_1.1 scene from OSDaR23 <https://data.fid-move.de/dataset/osdar23/resource/aedc84ed-bd0a-47bc-83d2-5488ad897042>`_. You need to download the dataset and substitute the path to the file as path_to_calibration_json.

You can find the solution :doc:`here <solution>`.

.. code-block:: python

    import raillabel

    path_to_calibration_json = ... # insert path to the downloaded 1_calibration_1.1_labels.json
    scene = raillabel.load(path_to_calibration_json)


    # Task 1: What is the ID of the first frame in the scene?
    first_frame_id = ...

    assert first_frame_id == 12


    # Task 2: What is the timestamp of the third frame in the scene?
    third_frame_timestamp = ...

    assert third_frame_timestamp == Decimal("1631441453.499971000")


    # Task 3: How many annotations are in the second frame?
    second_frame_annotation_number = ...

    assert second_frame_annotation_number == 210


    # Task 4: How many cuboid annotations are in the fourth frame?
    number_of_cuboid_annotations_in_fourth_frame = ...

    assert number_of_cuboid_annotations_in_fourth_frame == 15


    # Task 5: How many camera sensors are in the scene?
    number_of_camera_sensors = ...

    assert number_of_camera_sensors == 9


    # Task 6: How many unique persons are in the scene?
    number_of_persons = ...

    assert number_of_persons == 3
