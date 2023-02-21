# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

import raillabel


@pytest.fixture
def loader():
    return raillabel.format_loaders.LoaderRailLabelV2()


def test_filter_unexpected_kwarg(openlabel_v1_short_path):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    with pytest.raises(TypeError):
        raillabel.filter(scene, unsupported_kwarg=[])


def test_mutual_exclusivity(openlabel_v1_short_path):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    with pytest.raises(ValueError):
        raillabel.filter(scene, include_frames=[0], exclude_frames=[1, 2])


def test_filter_frames(openlabel_v1_short_path, openlabel_v1_short_data, loader):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    # Deletes the excluded data
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]
    del openlabel_v1_short_data["openlabel"]["objects"]["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = loader.load(openlabel_v1_short_data)

    # Tests for include filter
    scene_filtered = raillabel.filter(scene, include_frames=[0])
    assert scene_filtered == scene_filtered_ground_truth

    # Tests for exclude filter
    scene_filtered = raillabel.filter(scene, exclude_frames=[1])
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_start(openlabel_v1_short_path, openlabel_v1_short_data, loader):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    # Deletes the excluded data
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]
    del openlabel_v1_short_data["openlabel"]["objects"]["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = loader.load(openlabel_v1_short_data)

    # Tests for frame filter
    scene_filtered = raillabel.filter(scene, start_frame=1)
    assert scene_filtered == scene_filtered_ground_truth

    # Tests for timestamp filter
    scene_filtered = raillabel.filter(scene, start_timestamp="1632321743.134150")
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_end(openlabel_v1_short_path, openlabel_v1_short_data, loader):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    # Deletes the excluded data
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]
    del openlabel_v1_short_data["openlabel"]["objects"]["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = loader.load(openlabel_v1_short_data)

    # Tests for frame filter
    scene_filtered = raillabel.filter(scene, end_frame=0)
    assert scene_filtered == scene_filtered_ground_truth

    # Tests for timestamp filter
    scene_filtered = raillabel.filter(scene, end_timestamp="1632321743.233250")
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_object_ids(openlabel_v1_short_path, openlabel_v1_short_data, loader):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    # Deletes the excluded data
    del openlabel_v1_short_data["openlabel"]["objects"]["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = loader.load(openlabel_v1_short_data)

    # Tests for include filter
    scene_filtered = raillabel.filter(
        scene,
        include_object_ids=[
            "6fe55546-0dd7-4e40-b6b4-bb7ea3445772",
            "b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        ],
    )
    assert scene_filtered == scene_filtered_ground_truth

    # Tests for exclude filter
    scene_filtered = raillabel.filter(
        scene, exclude_object_ids=["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
    )
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_object_types(openlabel_v1_short_path, openlabel_v1_short_data, loader):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    # Deletes the excluded data
    del openlabel_v1_short_data["openlabel"]["objects"]["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = loader.load(openlabel_v1_short_data)

    # Tests for include filter
    scene_filtered = raillabel.filter(scene, include_object_types=["person"])
    assert scene_filtered == scene_filtered_ground_truth

    # Tests for exclude filter
    scene_filtered = raillabel.filter(scene, exclude_object_types=["train"])
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_annotation_ids(openlabel_v1_short_path, openlabel_v1_short_data, loader):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    # Deletes the excluded data
    del openlabel_v1_short_data["openlabel"]["objects"]["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = loader.load(openlabel_v1_short_data)

    # Tests for include filter
    scene_filtered = raillabel.filter(
        scene,
        include_annotation_ids=[
            "78f0ad89-2750-4a30-9d66-44c9da73a714",
            "68b4e02c-40c8-4de0-89ad-bc00ed05a043",
            "bebfbae4-61a2-4758-993c-efa846b050a5",
            "3f63201c-fb33-4487-aff6-ae0aa5fa976c",
            "dc2be700-8ee4-45c4-9256-920b5d55c917",
            "c1087f1d-7271-4dee-83ad-519a4e3b78a8",
            "50be7fe3-1f43-47ca-b65a-930e6cfacfeb",
            "6ba42cbc-484e-4b8d-a022-b23c2bb6643c",
            "5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e",
            "e2503c5d-9fe4-4666-b510-ef644c5a766b",
            "450ceb81-9778-4e63-bf89-42f3ed9f6747",
        ],
    )

    assert scene_filtered == scene_filtered_ground_truth

    # Tests for exclude filter
    scene_filtered = raillabel.filter(
        scene,
        exclude_annotation_ids=[
            "14f58fb0-add7-4ed9-85b3-74615986d854",
            "536ac83a-32c8-4fce-8499-ef32716c64a6",
            "e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c",
            "550df2c3-0e66-483e-bcc6-f3013b7e581b",
            "12b21c52-06ea-4269-9805-e7167e7a74ed",
        ],
    )
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_annotation_types(openlabel_v1_short_path, openlabel_v1_short_data, loader):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    # Deletes the excluded data
    del openlabel_v1_short_data["openlabel"]["objects"]["22dedd49-6dcb-413b-87ef-00ccfb532e98"]

    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["cuboid"]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["vec"]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]

    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = loader.load(openlabel_v1_short_data)

    # Tests for include filter
    scene_filtered = raillabel.filter(scene, include_annotation_types=["bbox", "poly2d", "Num"])

    assert scene_filtered == scene_filtered_ground_truth

    # Tests for exclude filter
    scene_filtered = raillabel.filter(scene, exclude_annotation_types=["cuboid", "Poly3d", "seg3d"])
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_sensors(openlabel_v1_short_path, openlabel_v1_short_data, loader):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    # Deletes the excluded data
    del openlabel_v1_short_data["openlabel"]["objects"]["22dedd49-6dcb-413b-87ef-00ccfb532e98"]

    del openlabel_v1_short_data["openlabel"]["streams"]["lidar"]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["frame_properties"]["streams"]["lidar"]
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["frame_properties"]["streams"]["lidar"]

    del openlabel_v1_short_data["openlabel"]["coordinate_systems"]["lidar"]
    del openlabel_v1_short_data["openlabel"]["coordinate_systems"]["base"]["children"][
        openlabel_v1_short_data["openlabel"]["coordinate_systems"]["base"]["children"].index(
            "lidar"
        )
    ]

    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["frame_properties"]["frame_data"][
        "num"
    ][-1]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["cuboid"]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["vec"]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]

    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["frame_properties"]["frame_data"][
        "num"
    ][-1]
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = loader.load(openlabel_v1_short_data)

    # Tests for include filter
    scene_filtered = raillabel.filter(scene, include_sensors=["rgb_middle", "ir_middle"])

    assert scene_filtered == scene_filtered_ground_truth

    # Tests for exclude filter
    scene_filtered = raillabel.filter(scene, exclude_sensors=["lidar"])
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_include_attribute_ids(openlabel_v1_short_path, openlabel_v1_short_data, loader):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    # Deletes the excluded data
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["bbox"][1]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["poly2d"][1]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["cuboid"][1]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["vec"][1]

    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "6fe55546-0dd7-4e40-b6b4-bb7ea3445772"
    ]["object_data"]["bbox"][1]
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]["object_data"]["cuboid"][1]
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]["object_data"]["vec"][1]

    del openlabel_v1_short_data["openlabel"]["streams"]["ir_middle"]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["frame_properties"]["streams"][
        "ir_middle"
    ]
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["frame_properties"]["streams"][
        "ir_middle"
    ]

    del openlabel_v1_short_data["openlabel"]["coordinate_systems"]["ir_middle"]
    del openlabel_v1_short_data["openlabel"]["coordinate_systems"]["base"]["children"][
        openlabel_v1_short_data["openlabel"]["coordinate_systems"]["base"]["children"].index(
            "ir_middle"
        )
    ]

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = loader.load(openlabel_v1_short_data)

    # Tests for include filter
    scene_filtered = raillabel.filter(scene, include_attributes={"test_text_attr0": None})

    assert scene_filtered == scene_filtered_ground_truth


def test_filter_exclude_attribute_ids(openlabel_v1_short_path, openlabel_v1_short_data, loader):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    # Deletes the excluded data
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["bbox"][0]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["poly2d"][0]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["cuboid"][0]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["vec"][0]

    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "6fe55546-0dd7-4e40-b6b4-bb7ea3445772"
    ]["object_data"]["bbox"][0]
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "6fe55546-0dd7-4e40-b6b4-bb7ea3445772"
    ]["object_data"]["poly2d"][0]
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]["object_data"]["cuboid"][0]
    del openlabel_v1_short_data["openlabel"]["frames"]["1"]["objects"][
        "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    ]["object_data"]["vec"][0]

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = loader.load(openlabel_v1_short_data)

    # Tests for exclude filter
    scene_filtered = raillabel.filter(scene, exclude_attributes={"test_text_attr0": None})
    assert scene_filtered == scene_filtered_ground_truth


def test_filter_exclude_attribute_values(openlabel_v1_short_path, openlabel_v1_short_data, loader):
    # Loads scene
    scene = raillabel.load(openlabel_v1_short_path, validate=False)

    # Deletes the excluded data
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["poly2d"][0]

    # Loads the ground truth filtered data
    scene_filtered_ground_truth = loader.load(openlabel_v1_short_data)

    # Tests for exclude filter
    scene_filtered = raillabel.filter(scene, exclude_attributes={"test_num_attr0": 2})
    assert scene_filtered == scene_filtered_ground_truth


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
