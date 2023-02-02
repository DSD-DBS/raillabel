# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import sys
from pathlib import Path
from xml.etree.ElementInclude import include

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

import raillabel

filtered_gt_dir = Path(__file__).parent / "__test_assets__"

openlabel_filtered_include_frames = filtered_gt_dir / "openlabel_v1_filtered_include_frames.json"


def test_filter_include_frames(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = raillabel.filter(scene, include_frames=0)

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_include_frames)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_exclude_frames(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(exclude_frames="1")

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_include_frames)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


openlabel_filtered_start_frame = filtered_gt_dir / "openlabel_v1_filtered_start_frame.json"
openlabel_filtered_end_frame = filtered_gt_dir / "openlabel_v1_filtered_end_frame.json"


def test_filter_start_frame(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(start_frame=1)

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_start_frame)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_end_frame(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(end_frame="0")

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_end_frame)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_start_timestamp(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(start_timestamp="1632321743.144149")

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_start_frame)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_end_timestamp(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(end_timestamp=1632321743.144149)

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_end_frame)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


openlabel_filtered_include_classes = filtered_gt_dir / "openlabel_v1_filtered_include_classes.json"
openlabel_filtered_exclude_classes = filtered_gt_dir / "openlabel_v1_filtered_exclude_classes.json"


def test_filter_include_classes(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(include_classes="person")

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_include_classes)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_exclude_classes(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(exclude_classes="person")

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_exclude_classes)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


openlabel_filtered_include_sensors = filtered_gt_dir / "openlabel_v1_filtered_include_sensors.json"
openlabel_filtered_exclude_sensors = filtered_gt_dir / "openlabel_v1_filtered_exclude_sensors.json"


def test_filter_include_sensors(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(include_sensors=["rgb_middle", "ir_middle"])

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_include_sensors)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_exclude_sensors(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(exclude_sensors=["rgb_middle", "ir_middle"])

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_exclude_sensors)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_include_annotation_types(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(include_annotation_types=["poly2d", "bbox"])

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(
        openlabel_filtered_include_sensors
    )  # Filtered scene is the same as openlabel_filtered_include_sensors

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_exclude_annotation_types(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(exclude_annotation_types=["bbox", "poly2d"])

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(
        openlabel_filtered_exclude_sensors
    )  # Filtered scene is the same as openlabel_filtered_include_sensors

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


openlabel_filtered_include_annotation_ids = (
    filtered_gt_dir / "openlabel_v1_filtered_include_annotation_ids.json"
)
openlabel_filtered_exclude_annotation_ids = (
    filtered_gt_dir / "openlabel_v1_filtered_exclude_annotation_ids.json"
)


def test_filter_include_annotation_ids(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(
        include_annotation_ids=[
            "78f0ad89-2750-4a30-9d66-44c9da73a714",
            "68b4e02c-40c8-4de0-89ad-bc00ed05a043",
            "536ac83a-32c8-4fce-8499-ef32716c64a6",
        ]
    )

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_include_annotation_ids)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_exclude_annotation_ids(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(exclude_annotation_ids="78f0ad89-2750-4a30-9d66-44c9da73a714")

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_exclude_annotation_ids)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


openlabel_filtered_include_object_ids = (
    filtered_gt_dir / "openlabel_v1_filtered_include_object_ids.json"
)


def test_filter_include_object_ids(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(include_object_ids="6fe55546-0dd7-4e40-b6b4-bb7ea3445772")

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_include_object_ids)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_exclude_object_ids(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(
        exclude_object_ids=[
            "b40ba3ad-0327-46ff-9c28-2506cfd6d934",
            "22dedd49-6dcb-413b-87ef-00ccfb532e98",
        ]
    )

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(
        openlabel_filtered_include_object_ids
    )  # Filtered scene is the same as openlabel_filtered_include_object_ids

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


openlabel_filtered_include_attributes = (
    filtered_gt_dir / "openlabel_v1_filtered_include_attributes.json"
)
openlabel_filtered_exclude_attributes = (
    filtered_gt_dir / "openlabel_v1_filtered_exclude_attributes.json"
)


def test_filter_include_attributes(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(include_attributes={"test_bool_attr0": True})

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_include_attributes)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_exclude_attributes(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(exclude_attributes={"test_text_attr0": None})

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_exclude_attributes)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


openlabel_filtered_multi0 = filtered_gt_dir / "openlabel_v1_filtered_multi0.json"


def test_filter_multi0(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(
        include_frames=["1"],
        exclude_annotation_types=["bbox"],
        include_sensors=["lidar", "rgb_middle"],
        exclude_annotation_ids="e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c",
    )

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_multi0)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


openlabel_filtered_empty = filtered_gt_dir / "openlabel_v1_filtered_empty.json"


def test_filter_empty(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene_filtered = scene.filter(
        include_frames=["1"],
        exclude_annotation_types=["bbox"],
        exclude_sensors=["lidar", "rgb_middle"],
        exclude_annotation_ids="e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c",
    )

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = raillabel.load(openlabel_filtered_empty)

    # Compares the two
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_error(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    with pytest.raises(ValueError):
        scene.filter(include_classes="abc", exclude_classes="dggb")


def test_filter_orig_scene_unchanged(openlabel_v1_short_path):
    # Loads and filters the scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)
    scene.filter(exclude_attributes={"test_text_attr0": None})

    # Compares the scene with a freshly loaded one
    assert scene == raillabel.load(openlabel_v1_short_path, validate=False)


# Executes the test if the file is called
if __name__ == "__main__":
    pytest.main([__file__, "--disable-pytest-warnings"])
