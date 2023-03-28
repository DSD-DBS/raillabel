# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import decimal
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel


@pytest.fixture
def loader():
    return raillabel.format_loaders.LoaderRailLabelV2()


def test_supports_true(openlabel_v1_short_data, loader):
    assert loader.supports(openlabel_v1_short_data)


def test_supports_false(openlabel_v1_short_data, loader):
    openlabel_v1_short_data["openlabel"]["metadata"]["subschema_version"] = "3.0.0"
    assert not loader.supports(openlabel_v1_short_data)


def test_load_metadata(openlabel_v1_short_data, loader, raillabel_v2_schema_data):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert scene.metadata.annotator == "test_annotator"
    assert scene.metadata.comment == "test_comment"
    assert scene.metadata.name == "test_project"
    assert scene.metadata.schema_version == "1.0.0"
    assert scene.metadata.tagged_file == "test_folder"
    assert scene.metadata.subschema_version == raillabel_v2_schema_data["version"]


def test_load_sensors(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert len(scene.sensors) == 3

    assert "rgb_middle" in scene.sensors
    assert scene.sensors["rgb_middle"].uid == "rgb_middle"
    assert scene.sensors["rgb_middle"].type == "camera"
    assert scene.sensors["rgb_middle"].uri == "/S1206063/image"
    assert scene.sensors["rgb_middle"].intrinsics.camera_matrix == (
        0.48,
        0,
        0.81,
        0,
        0,
        0.16,
        0.83,
        0,
        0,
        0,
        1,
        0,
    )
    assert scene.sensors["rgb_middle"].intrinsics.distortion == (
        0.49,
        0.69,
        0.31,
        0.81,
        0.99,
    )
    assert scene.sensors["rgb_middle"].intrinsics.width_px == 2464
    assert scene.sensors["rgb_middle"].intrinsics.height_px == 1600
    assert scene.sensors["rgb_middle"].extrinsics.pos == raillabel.format.Point3d(0, 1, 2)
    assert scene.sensors["rgb_middle"].extrinsics.quat == raillabel.format.Quaternion(
        0.97518507, -0.18529384, -0.05469746, -0.10811315
    )

    assert "ir_middle" in scene.sensors
    assert scene.sensors["ir_middle"].uid == "ir_middle"
    assert scene.sensors["ir_middle"].type == "camera"
    assert scene.sensors["ir_middle"].uri == "/A0001781/image"
    assert scene.sensors["ir_middle"].intrinsics.camera_matrix == (
        0.47,
        0,
        0.85,
        0,
        0,
        0.15,
        0.23,
        0,
        0,
        0,
        1,
        0,
    )
    assert scene.sensors["ir_middle"].intrinsics.distortion == (
        0.19,
        0.66,
        0.31,
        0.21,
        0.99,
    )
    assert scene.sensors["ir_middle"].intrinsics.width_px == 640
    assert scene.sensors["ir_middle"].intrinsics.height_px == 480
    assert scene.sensors["ir_middle"].extrinsics.pos == raillabel.format.Point3d(0, 2, 1)
    assert scene.sensors["ir_middle"].extrinsics.quat == raillabel.format.Quaternion(
        -0.64984101, -0.72563166, 0.18784818, -0.12600959
    )

    assert "lidar" in scene.sensors
    assert scene.sensors["lidar"].uid == "lidar"
    assert scene.sensors["lidar"].type == "lidar"
    assert scene.sensors["lidar"].uri == "/lidar_merged"
    assert scene.sensors["lidar"].extrinsics.pos == raillabel.format.Point3d(0, 0, 0)
    assert scene.sensors["lidar"].extrinsics.quat == raillabel.format.Quaternion(0, 0, 0, 1)


def test_load_objects(openlabel_v1_short_data, loader):
    # Removes the object data pointers from the example file so that it needs to be generated from the data
    for object in openlabel_v1_short_data["openlabel"]["objects"].values():
        del object["frame_intervals"]
        del object["object_data_pointers"]

    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert len(scene.objects) == 3

    assert "b40ba3ad-0327-46ff-9c28-2506cfd6d934" in scene.objects
    assert (
        scene.objects["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].uid
        == "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    )
    assert scene.objects["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].name == "person_0000"
    assert scene.objects["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].type == "person"

    assert "6fe55546-0dd7-4e40-b6b4-bb7ea3445772" in scene.objects
    assert (
        scene.objects["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].uid
        == "6fe55546-0dd7-4e40-b6b4-bb7ea3445772"
    )
    assert scene.objects["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].name == "person_0001"
    assert scene.objects["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].type == "person"

    assert "22dedd49-6dcb-413b-87ef-00ccfb532e98" in scene.objects
    assert (
        scene.objects["22dedd49-6dcb-413b-87ef-00ccfb532e98"].uid
        == "22dedd49-6dcb-413b-87ef-00ccfb532e98"
    )
    assert scene.objects["22dedd49-6dcb-413b-87ef-00ccfb532e98"].name == "train_0000"
    assert scene.objects["22dedd49-6dcb-413b-87ef-00ccfb532e98"].type == "train"


def test_load_frame0_metadata(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert 0 in scene.frames
    assert scene.frames[0].timestamp == decimal.Decimal("1632321743.134149")

    assert len(scene.frames[0].sensors) == 3
    assert "rgb_middle" in scene.frames[0].sensors
    assert scene.frames[0].sensors["rgb_middle"].sensor == scene.sensors["rgb_middle"]
    assert scene.frames[0].sensors["rgb_middle"].timestamp == decimal.Decimal(
        "1632321743.100000072"
    )
    assert scene.frames[0].sensors["rgb_middle"].uri == "rgb_test0.png"
    assert "ir_middle" in scene.frames[0].sensors
    assert scene.frames[0].sensors["ir_middle"].sensor == scene.sensors["ir_middle"]
    assert scene.frames[0].sensors["ir_middle"].timestamp == decimal.Decimal("1632321743.106000004")
    assert scene.frames[0].sensors["ir_middle"].uri == "ir_test0.png"
    assert "lidar" in scene.frames[0].sensors
    assert scene.frames[0].sensors["lidar"].sensor == scene.sensors["lidar"]
    assert scene.frames[0].sensors["lidar"].timestamp == decimal.Decimal("1632321743.134149")
    assert scene.frames[0].sensors["lidar"].uri == "lidar_test0.pcd"

    assert len(scene.frames[0].data) == 2
    assert "test_frame_data0" in scene.frames[0].data
    assert scene.frames[0].data["test_frame_data0"].uid == "a06fe567-29c7-475b-92a4-fbca64e671a7"
    assert scene.frames[0].data["a06fe567-29c7-475b-92a4-fbca64e671a7"].name == "test_frame_data0"
    assert scene.frames[0].data["test_frame_data0"].val == 53.1
    assert scene.frames[0].data["test_frame_data0"].sensor == scene.sensors["rgb_middle"]
    assert "test_frame_data1" in scene.frames[0].data
    assert scene.frames[0].data["test_frame_data1"].uid == "4bb95df7-a051-48a9-b77e-72f27ca43f64"
    assert scene.frames[0].data["4bb95df7-a051-48a9-b77e-72f27ca43f64"].name == "test_frame_data1"
    assert scene.frames[0].data["test_frame_data1"].val == 10
    assert scene.frames[0].data["test_frame_data1"].sensor == scene.sensors["lidar"]

    assert len(scene.frames[0].object_data) == 2
    assert "b40ba3ad-0327-46ff-9c28-2506cfd6d934" in scene.frames[0].object_data
    assert (
        scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].object
        == scene.objects["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
    )
    assert "22dedd49-6dcb-413b-87ef-00ccfb532e98" in scene.frames[0].object_data
    assert (
        scene.frames[0].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].object
        == scene.objects["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
    )


def test_load_frame0_bboxs(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert len(scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].bboxs) == 2

    assert (
        "78f0ad89-2750-4a30-9d66-44c9da73a714"
        in scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].bboxs
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["78f0ad89-2750-4a30-9d66-44c9da73a714"]
        == scene.frames[0].annotations["78f0ad89-2750-4a30-9d66-44c9da73a714"]
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["78f0ad89-2750-4a30-9d66-44c9da73a714"]
        .uid
        == "78f0ad89-2750-4a30-9d66-44c9da73a714"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["78f0ad89-2750-4a30-9d66-44c9da73a714"]
        .name
        == "rgb_middle__bbox__person"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["78f0ad89-2750-4a30-9d66-44c9da73a714"]
        .pos.x
        == 0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["78f0ad89-2750-4a30-9d66-44c9da73a714"]
        .pos.y
        == 1
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["78f0ad89-2750-4a30-9d66-44c9da73a714"]
        .size.x
        == 2
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["78f0ad89-2750-4a30-9d66-44c9da73a714"]
        .size.y
        == 3
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["78f0ad89-2750-4a30-9d66-44c9da73a714"]
        .sensor
        == scene.sensors["rgb_middle"]
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].bboxs[
        "78f0ad89-2750-4a30-9d66-44c9da73a714"
    ].attributes == {
        "test_text_attr0": "test_text_attr0_val",
        "test_text_attr1": "test_text_attr1_val",
        "test_num_attr0": 0,
        "test_num_attr1": 1,
        "test_bool_attr0": True,
        "test_vec_attr0": ["0", "1"],
        "test_vec_attr1": [0, 1, 2],
        "test_vec_attr2": ["a", "b", "c"],
    }

    assert (
        "68b4e02c-40c8-4de0-89ad-bc00ed05a043"
        in scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].bboxs
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["68b4e02c-40c8-4de0-89ad-bc00ed05a043"]
        == scene.frames[0].annotations["68b4e02c-40c8-4de0-89ad-bc00ed05a043"]
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["68b4e02c-40c8-4de0-89ad-bc00ed05a043"]
        .uid
        == "68b4e02c-40c8-4de0-89ad-bc00ed05a043"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["68b4e02c-40c8-4de0-89ad-bc00ed05a043"]
        .name
        == "ir_middle__bbox__person"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["68b4e02c-40c8-4de0-89ad-bc00ed05a043"]
        .pos.x
        == 3
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["68b4e02c-40c8-4de0-89ad-bc00ed05a043"]
        .pos.y
        == 2
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["68b4e02c-40c8-4de0-89ad-bc00ed05a043"]
        .size.x
        == 1
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["68b4e02c-40c8-4de0-89ad-bc00ed05a043"]
        .size.y
        == 0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["68b4e02c-40c8-4de0-89ad-bc00ed05a043"]
        .sensor
        is scene.sensors["ir_middle"]
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].bboxs[
        "68b4e02c-40c8-4de0-89ad-bc00ed05a043"
    ].attributes == {"test_bool_attr0": False}


def test_load_frame0_poly2ds(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert len(scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].poly2ds) == 2

    assert (
        "bebfbae4-61a2-4758-993c-efa846b050a5"
        in scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].poly2ds
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["bebfbae4-61a2-4758-993c-efa846b050a5"]
        == scene.frames[0].annotations["bebfbae4-61a2-4758-993c-efa846b050a5"]
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["bebfbae4-61a2-4758-993c-efa846b050a5"]
        .uid
        == "bebfbae4-61a2-4758-993c-efa846b050a5"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["bebfbae4-61a2-4758-993c-efa846b050a5"]
        .name
        == "rgb_middle__poly2d__person"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["bebfbae4-61a2-4758-993c-efa846b050a5"]
        .closed
        == False
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["bebfbae4-61a2-4758-993c-efa846b050a5"]
        .mode
        == "MODE_POLY2D_ABSOLUTE"
    )
    assert (
        len(
            scene.frames[0]
            .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
            .poly2ds["bebfbae4-61a2-4758-993c-efa846b050a5"]
            .points
        )
        == 2
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].poly2ds[
        "bebfbae4-61a2-4758-993c-efa846b050a5"
    ].points[0] == raillabel.format.Point2d(1, 2)
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].poly2ds[
        "bebfbae4-61a2-4758-993c-efa846b050a5"
    ].points[1] == raillabel.format.Point2d(3, 4)
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["bebfbae4-61a2-4758-993c-efa846b050a5"]
        .sensor
        == scene.sensors["rgb_middle"]
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].poly2ds[
        "bebfbae4-61a2-4758-993c-efa846b050a5"
    ].attributes == {
        "test_text_attr0": "test_text_attr0_val",
        "test_text_attr1": "test_text_attr1_val",
        "test_num_attr0": 2,
        "test_num_attr1": 1,
        "test_bool_attr0": True,
        "test_vec_attr0": ["0", "1"],
        "test_vec_attr1": [0, 1, 2],
        "test_vec_attr2": ["a", "b", "c"],
    }

    assert (
        "3f63201c-fb33-4487-aff6-ae0aa5fa976c"
        in scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].poly2ds
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["3f63201c-fb33-4487-aff6-ae0aa5fa976c"]
        == scene.frames[0].annotations["3f63201c-fb33-4487-aff6-ae0aa5fa976c"]
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["3f63201c-fb33-4487-aff6-ae0aa5fa976c"]
        .uid
        == "3f63201c-fb33-4487-aff6-ae0aa5fa976c"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["3f63201c-fb33-4487-aff6-ae0aa5fa976c"]
        .name
        == "ir_middle__poly2d__person"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["3f63201c-fb33-4487-aff6-ae0aa5fa976c"]
        .closed
        == True
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["3f63201c-fb33-4487-aff6-ae0aa5fa976c"]
        .mode
        == "MODE_POLY2D_ABSOLUTE"
    )
    assert (
        len(
            scene.frames[0]
            .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
            .poly2ds["3f63201c-fb33-4487-aff6-ae0aa5fa976c"]
            .points
        )
        == 4
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].poly2ds[
        "3f63201c-fb33-4487-aff6-ae0aa5fa976c"
    ].points[0] == raillabel.format.Point2d(7, 6)
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].poly2ds[
        "3f63201c-fb33-4487-aff6-ae0aa5fa976c"
    ].points[1] == raillabel.format.Point2d(5, 4)
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].poly2ds[
        "3f63201c-fb33-4487-aff6-ae0aa5fa976c"
    ].points[2] == raillabel.format.Point2d(3, 2)
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].poly2ds[
        "3f63201c-fb33-4487-aff6-ae0aa5fa976c"
    ].points[3] == raillabel.format.Point2d(1, 0)
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .poly2ds["3f63201c-fb33-4487-aff6-ae0aa5fa976c"]
        .sensor
        == scene.sensors["ir_middle"]
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].poly2ds[
        "3f63201c-fb33-4487-aff6-ae0aa5fa976c"
    ].attributes == {"test_bool_attr0": False}


def test_load_frame0_cuboids(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert len(scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].cuboids) == 2

    assert (
        "dc2be700-8ee4-45c4-9256-920b5d55c917"
        in scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].cuboids
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        == scene.frames[0].annotations["dc2be700-8ee4-45c4-9256-920b5d55c917"]
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .uid
        == "dc2be700-8ee4-45c4-9256-920b5d55c917"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .name
        == "lidar__cuboid__person"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .pos.x
        == 0.49
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .pos.y
        == 0.04
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .pos.z
        == 0.73
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .quat.x
        == 0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .quat.y
        == 0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .quat.z
        == 0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .quat.w
        == 0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .size.x
        == 0.75
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .size.y
        == 0.01
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .size.z
        == 0.10
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["dc2be700-8ee4-45c4-9256-920b5d55c917"]
        .sensor
        == scene.sensors["lidar"]
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].cuboids[
        "dc2be700-8ee4-45c4-9256-920b5d55c917"
    ].attributes == {
        "test_text_attr0": "test_text_attr0_val",
        "test_text_attr1": "test_text_attr1_val",
        "test_num_attr0": 0,
        "test_num_attr1": 1,
        "test_bool_attr0": True,
        "test_vec_attr0": ["0", "1"],
        "test_vec_attr1": [0, 1, 2],
        "test_vec_attr2": ["a", "b", "c"],
    }

    assert (
        "450ceb81-9778-4e63-bf89-42f3ed9f6747"
        in scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].cuboids
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        == scene.frames[0].annotations["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .uid
        == "450ceb81-9778-4e63-bf89-42f3ed9f6747"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .name
        == "lidar__cuboid__person"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .pos.x
        == 0.0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .pos.y
        == 1.0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .pos.z
        == 2.0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .quat.x
        == 3.0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .quat.y
        == 4.0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .quat.z
        == 5.0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .quat.w
        == 6.0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .size.x
        == 7.0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .size.y
        == 8.0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .size.z
        == 9.0
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .cuboids["450ceb81-9778-4e63-bf89-42f3ed9f6747"]
        .sensor
        == scene.sensors["lidar"]
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].cuboids[
        "450ceb81-9778-4e63-bf89-42f3ed9f6747"
    ].attributes == {"test_bool_attr0": False}


def test_load_frame0_seg3ds(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert len(scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].seg3ds) == 2

    assert (
        "c1087f1d-7271-4dee-83ad-519a4e3b78a8"
        in scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].seg3ds
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .seg3ds["c1087f1d-7271-4dee-83ad-519a4e3b78a8"]
        == scene.frames[0].annotations["c1087f1d-7271-4dee-83ad-519a4e3b78a8"]
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .seg3ds["c1087f1d-7271-4dee-83ad-519a4e3b78a8"]
        .uid
        == "c1087f1d-7271-4dee-83ad-519a4e3b78a8"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .seg3ds["c1087f1d-7271-4dee-83ad-519a4e3b78a8"]
        .name
        == "lidar__vec__person"
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].seg3ds[
        "c1087f1d-7271-4dee-83ad-519a4e3b78a8"
    ].point_ids == list(range(10))
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .seg3ds["c1087f1d-7271-4dee-83ad-519a4e3b78a8"]
        .sensor
        == scene.sensors["lidar"]
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].seg3ds[
        "c1087f1d-7271-4dee-83ad-519a4e3b78a8"
    ].attributes == {
        "test_text_attr0": "test_text_attr0_val",
        "test_text_attr1": "test_text_attr1_val",
        "test_num_attr0": 0,
        "test_num_attr1": 1,
        "test_bool_attr0": True,
        "test_vec_attr0": ["0", "1"],
        "test_vec_attr1": [0, 1, 2],
        "test_vec_attr2": ["a", "b", "c"],
    }

    assert (
        "50be7fe3-1f43-47ca-b65a-930e6cfacfeb"
        in scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].seg3ds
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .seg3ds["50be7fe3-1f43-47ca-b65a-930e6cfacfeb"]
        == scene.frames[0].annotations["50be7fe3-1f43-47ca-b65a-930e6cfacfeb"]
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .seg3ds["50be7fe3-1f43-47ca-b65a-930e6cfacfeb"]
        .uid
        == "50be7fe3-1f43-47ca-b65a-930e6cfacfeb"
    )
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .seg3ds["50be7fe3-1f43-47ca-b65a-930e6cfacfeb"]
        .name
        == "lidar__vec__person"
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].seg3ds[
        "50be7fe3-1f43-47ca-b65a-930e6cfacfeb"
    ].point_ids == list(reversed(range(10)))
    assert (
        scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .seg3ds["50be7fe3-1f43-47ca-b65a-930e6cfacfeb"]
        .sensor
        == scene.sensors["lidar"]
    )
    assert scene.frames[0].object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"].seg3ds[
        "50be7fe3-1f43-47ca-b65a-930e6cfacfeb"
    ].attributes == {"test_bool_attr0": False}


def test_load_frame0_poly3ds(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert len(scene.frames[0].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].poly3ds) == 1

    assert (
        "14f58fb0-add7-4ed9-85b3-74615986d854"
        in scene.frames[0].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].poly3ds
    )
    assert (
        scene.frames[0]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .poly3ds["14f58fb0-add7-4ed9-85b3-74615986d854"]
        == scene.frames[0].annotations["14f58fb0-add7-4ed9-85b3-74615986d854"]
    )
    assert (
        scene.frames[0]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .poly3ds["14f58fb0-add7-4ed9-85b3-74615986d854"]
        .uid
        == "14f58fb0-add7-4ed9-85b3-74615986d854"
    )
    assert (
        scene.frames[0]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .poly3ds["14f58fb0-add7-4ed9-85b3-74615986d854"]
        .name
        == "lidar__poly3d__train"
    )
    assert (
        scene.frames[0]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .poly3ds["14f58fb0-add7-4ed9-85b3-74615986d854"]
        .closed
        == False
    )
    assert (
        len(
            scene.frames[0]
            .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
            .poly3ds["14f58fb0-add7-4ed9-85b3-74615986d854"]
            .points
        )
        == 3
    )
    assert scene.frames[0].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].poly3ds[
        "14f58fb0-add7-4ed9-85b3-74615986d854"
    ].points[0] == raillabel.format.Point3d(9, 8, 7)
    assert scene.frames[0].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].poly3ds[
        "14f58fb0-add7-4ed9-85b3-74615986d854"
    ].points[1] == raillabel.format.Point3d(6, 5, 4)
    assert scene.frames[0].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].poly3ds[
        "14f58fb0-add7-4ed9-85b3-74615986d854"
    ].points[2] == raillabel.format.Point3d(3, 2, 1)
    assert (
        scene.frames[0]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .poly3ds["14f58fb0-add7-4ed9-85b3-74615986d854"]
        .sensor
        == scene.sensors["lidar"]
    )


def test_load_frame1_metadata(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert 1 in scene.frames
    assert scene.frames[1].timestamp == decimal.Decimal("1632321743.233263")

    assert len(scene.frames[1].sensors) == 3
    assert "rgb_middle" in scene.frames[1].sensors
    assert scene.frames[1].sensors["rgb_middle"].sensor == scene.sensors["rgb_middle"]
    assert scene.frames[1].sensors["rgb_middle"].timestamp == decimal.Decimal("1632321743.2")
    assert scene.frames[1].sensors["rgb_middle"].uri == "rgb_test1.png"
    assert "ir_middle" in scene.frames[1].sensors
    assert scene.frames[1].sensors["ir_middle"].sensor == scene.sensors["ir_middle"]
    assert scene.frames[1].sensors["ir_middle"].timestamp == decimal.Decimal("1632321743.208000004")
    assert scene.frames[1].sensors["ir_middle"].uri == "ir_test1.png"
    assert "lidar" in scene.frames[1].sensors
    assert scene.frames[1].sensors["lidar"].sensor == scene.sensors["lidar"]
    assert scene.frames[1].sensors["lidar"].timestamp == decimal.Decimal("1632321743.233263")
    assert scene.frames[1].sensors["lidar"].uri == "lidar_test1.pcd"

    assert len(scene.frames[1].data) == 2
    assert "test_frame_data0" in scene.frames[1].data
    assert scene.frames[1].data["test_frame_data0"].uid == "558697df-61f5-41b0-b112-3d6fcbd7d6c9"
    assert scene.frames[1].data["558697df-61f5-41b0-b112-3d6fcbd7d6c9"].name == "test_frame_data0"
    assert scene.frames[1].data["test_frame_data0"].val == 53
    assert scene.frames[1].data["test_frame_data0"].sensor == scene.sensors["rgb_middle"]
    assert "test_frame_data1" in scene.frames[1].data
    assert scene.frames[1].data["test_frame_data1"].uid == "843e07a0-aac5-4f62-8200-1468dbd3055d"
    assert scene.frames[1].data["843e07a0-aac5-4f62-8200-1468dbd3055d"].name == "test_frame_data1"
    assert scene.frames[1].data["test_frame_data1"].val == 10.1
    assert scene.frames[1].data["test_frame_data1"].sensor == scene.sensors["lidar"]

    assert len(scene.frames[1].object_data) == 2
    assert "6fe55546-0dd7-4e40-b6b4-bb7ea3445772" in scene.frames[1].object_data
    assert (
        scene.frames[1].object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].object
        == scene.objects["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
    )
    assert "22dedd49-6dcb-413b-87ef-00ccfb532e98" in scene.frames[1].object_data
    assert (
        scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].object
        == scene.objects["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
    )


def test_load_frame1_bboxs(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert len(scene.frames[1].object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].bboxs) == 2

    assert (
        "6ba42cbc-484e-4b8d-a022-b23c2bb6643c"
        in scene.frames[1].object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].bboxs
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["6ba42cbc-484e-4b8d-a022-b23c2bb6643c"]
        == scene.frames[1].annotations["6ba42cbc-484e-4b8d-a022-b23c2bb6643c"]
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["6ba42cbc-484e-4b8d-a022-b23c2bb6643c"]
        .uid
        == "6ba42cbc-484e-4b8d-a022-b23c2bb6643c"
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["6ba42cbc-484e-4b8d-a022-b23c2bb6643c"]
        .name
        == "rgb_middle__bbox__person"
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["6ba42cbc-484e-4b8d-a022-b23c2bb6643c"]
        .pos.x
        == 0
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["6ba42cbc-484e-4b8d-a022-b23c2bb6643c"]
        .pos.y
        == 1
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["6ba42cbc-484e-4b8d-a022-b23c2bb6643c"]
        .size.x
        == 2
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["6ba42cbc-484e-4b8d-a022-b23c2bb6643c"]
        .size.y
        == 3
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["6ba42cbc-484e-4b8d-a022-b23c2bb6643c"]
        .sensor
        == scene.sensors["rgb_middle"]
    )
    assert scene.frames[1].object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].bboxs[
        "6ba42cbc-484e-4b8d-a022-b23c2bb6643c"
    ].attributes == {
        "test_text_attr0": "test_text_attr0_val",
        "test_text_attr1": "test_text_attr1_val",
        "test_num_attr0": 0,
        "test_num_attr1": 1,
        "test_bool_attr0": True,
        "test_vec_attr0": ["0", "1"],
        "test_vec_attr1": [0, 1, 2],
        "test_vec_attr2": ["a", "b", "c"],
    }

    assert (
        "5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"
        in scene.frames[1].object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].bboxs
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"]
        == scene.frames[1].annotations["5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"]
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"]
        .uid
        == "5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"]
        .name
        == "ir_middle__bbox__person"
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"]
        .pos.x
        == 3
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"]
        .pos.y
        == 2
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"]
        .size.x
        == 1
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"]
        .size.y
        == 0
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .bboxs["5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"]
        .sensor
        == scene.sensors["ir_middle"]
    )
    assert scene.frames[1].object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].bboxs[
        "5f28fa18-8f2a-4a40-a0b6-c0bbedc00f2e"
    ].attributes == {"test_bool_attr0": False}


def test_load_frame1_poly2ds(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert len(scene.frames[1].object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].poly2ds) == 1

    assert (
        "e2503c5d-9fe4-4666-b510-ef644c5a766b"
        in scene.frames[1].object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].poly2ds
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .poly2ds["e2503c5d-9fe4-4666-b510-ef644c5a766b"]
        == scene.frames[1].annotations["e2503c5d-9fe4-4666-b510-ef644c5a766b"]
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .poly2ds["e2503c5d-9fe4-4666-b510-ef644c5a766b"]
        .uid
        == "e2503c5d-9fe4-4666-b510-ef644c5a766b"
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .poly2ds["e2503c5d-9fe4-4666-b510-ef644c5a766b"]
        .name
        == "rgb_middle__poly2d__person"
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .poly2ds["e2503c5d-9fe4-4666-b510-ef644c5a766b"]
        .closed
        == False
    )
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .poly2ds["e2503c5d-9fe4-4666-b510-ef644c5a766b"]
        .mode
        == "MODE_POLY2D_ABSOLUTE"
    )
    assert (
        len(
            scene.frames[1]
            .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
            .poly2ds["e2503c5d-9fe4-4666-b510-ef644c5a766b"]
            .points
        )
        == 2
    )
    assert scene.frames[1].object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].poly2ds[
        "e2503c5d-9fe4-4666-b510-ef644c5a766b"
    ].points[0] == raillabel.format.Point2d(1, 2)
    assert scene.frames[1].object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].poly2ds[
        "e2503c5d-9fe4-4666-b510-ef644c5a766b"
    ].points[1] == raillabel.format.Point2d(3, 4)
    assert (
        scene.frames[1]
        .object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"]
        .poly2ds["e2503c5d-9fe4-4666-b510-ef644c5a766b"]
        .sensor
        == scene.sensors["rgb_middle"]
    )
    assert scene.frames[1].object_data["6fe55546-0dd7-4e40-b6b4-bb7ea3445772"].poly2ds[
        "e2503c5d-9fe4-4666-b510-ef644c5a766b"
    ].attributes == {
        "test_text_attr0": "test_text_attr0_val",
        "test_text_attr1": "test_text_attr1_val",
        "test_num_attr0": 0,
        "test_num_attr1": 1,
        "test_bool_attr0": True,
        "test_vec_attr0": ["0", "1"],
        "test_vec_attr1": [0, 1, 2],
        "test_vec_attr2": ["a", "b", "c"],
    }


def test_load_frame1_cuboids(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert len(scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].cuboids) == 2

    assert (
        "536ac83a-32c8-4fce-8499-ef32716c64a6"
        in scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].cuboids
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        == scene.frames[1].annotations["536ac83a-32c8-4fce-8499-ef32716c64a6"]
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .uid
        == "536ac83a-32c8-4fce-8499-ef32716c64a6"
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .name
        == "lidar__cuboid__train"
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .pos.x
        == 0
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .pos.y
        == 1
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .pos.z
        == 2
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .quat.x
        == 3
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .quat.y
        == 4
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .quat.z
        == 5
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .quat.w
        == 6
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .size.x
        == 7
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .size.y
        == 8
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .size.z
        == 9
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["536ac83a-32c8-4fce-8499-ef32716c64a6"]
        .sensor
        == scene.sensors["lidar"]
    )
    assert scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].cuboids[
        "536ac83a-32c8-4fce-8499-ef32716c64a6"
    ].attributes == {
        "test_text_attr0": "test_text_attr0_val",
        "test_text_attr1": "test_text_attr1_val",
        "test_num_attr0": 0,
        "test_num_attr1": 1,
        "test_bool_attr0": True,
        "test_vec_attr0": ["0", "1"],
        "test_vec_attr1": [0, 1, 2],
        "test_vec_attr2": ["a", "b", "c"],
    }

    assert (
        "e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"
        in scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].cuboids
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        == scene.frames[1].annotations["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .uid
        == "e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .name
        == "lidar__cuboid__train"
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .pos.x
        == 0.0
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .pos.y
        == 1.0
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .pos.z
        == 2.0
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .quat.x
        == 3.0
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .quat.y
        == 4.0
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .quat.z
        == 5.0
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .quat.w
        == 6.0
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .size.x
        == 7.0
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .size.y
        == 8.0
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .size.z
        == 9.0
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .cuboids["e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"]
        .sensor
        == scene.sensors["lidar"]
    )
    assert scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].cuboids[
        "e53bd5e3-980a-4fa7-a0f9-5a2e59ba663c"
    ].attributes == {"test_bool_attr0": False}


def test_load_frame1_seg3ds(openlabel_v1_short_data, loader):
    scene = loader.load(openlabel_v1_short_data, validate=False)

    assert len(scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].seg3ds) == 2

    assert (
        "550df2c3-0e66-483e-bcc6-f3013b7e581b"
        in scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].seg3ds
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .seg3ds["550df2c3-0e66-483e-bcc6-f3013b7e581b"]
        == scene.frames[1].annotations["550df2c3-0e66-483e-bcc6-f3013b7e581b"]
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .seg3ds["550df2c3-0e66-483e-bcc6-f3013b7e581b"]
        .uid
        == "550df2c3-0e66-483e-bcc6-f3013b7e581b"
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .seg3ds["550df2c3-0e66-483e-bcc6-f3013b7e581b"]
        .name
        == "lidar__vec__train"
    )
    assert scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].seg3ds[
        "550df2c3-0e66-483e-bcc6-f3013b7e581b"
    ].point_ids == list(range(10))
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .seg3ds["550df2c3-0e66-483e-bcc6-f3013b7e581b"]
        .sensor
        == scene.sensors["lidar"]
    )
    assert scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].seg3ds[
        "550df2c3-0e66-483e-bcc6-f3013b7e581b"
    ].attributes == {
        "test_text_attr0": "test_text_attr0_val",
        "test_text_attr1": "test_text_attr1_val",
        "test_num_attr0": 0,
        "test_num_attr1": 1,
        "test_bool_attr0": True,
        "test_vec_attr0": ["0", "1"],
        "test_vec_attr1": [0, 1, 2],
        "test_vec_attr2": ["a", "b", "c"],
    }

    assert (
        "12b21c52-06ea-4269-9805-e7167e7a74ed"
        in scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].seg3ds
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .seg3ds["12b21c52-06ea-4269-9805-e7167e7a74ed"]
        == scene.frames[1].annotations["12b21c52-06ea-4269-9805-e7167e7a74ed"]
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .seg3ds["12b21c52-06ea-4269-9805-e7167e7a74ed"]
        .uid
        == "12b21c52-06ea-4269-9805-e7167e7a74ed"
    )
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .seg3ds["12b21c52-06ea-4269-9805-e7167e7a74ed"]
        .name
        == "lidar__vec__train"
    )
    assert scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].seg3ds[
        "12b21c52-06ea-4269-9805-e7167e7a74ed"
    ].point_ids == list(reversed(range(10)))
    assert (
        scene.frames[1]
        .object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"]
        .seg3ds["12b21c52-06ea-4269-9805-e7167e7a74ed"]
        .sensor
        == scene.sensors["lidar"]
    )
    assert scene.frames[1].object_data["22dedd49-6dcb-413b-87ef-00ccfb532e98"].seg3ds[
        "12b21c52-06ea-4269-9805-e7167e7a74ed"
    ].attributes == {"test_bool_attr0": False}


def test_load_uri_vcd_incompatible(
    openlabel_v1_short_data, openlabel_v1_vcd_incompatible_data, loader
):
    """Tests, whether an older annotation file, which is not usable for the VCD
    library is converted into a compatible one."""

    scene_ground_truth = loader.load(openlabel_v1_short_data, validate=False)
    scene = loader.load(openlabel_v1_vcd_incompatible_data, validate=False)

    # The UUIDs of the frame data have been generated and therefore do not match the ground truth.
    # They are set equal here.
    for frame_id in scene_ground_truth.frames:
        for frame_data in scene_ground_truth.frames[frame_id].data:
            for other_frame_data in list(scene.frames[frame_id].data):
                if (
                    scene.frames[frame_id].data[other_frame_data].name
                    == scene_ground_truth.frames[frame_id].data[frame_data].name
                ):
                    scene.frames[frame_id].data[frame_data] = scene.frames[frame_id].data[
                        other_frame_data
                    ]
                    del scene.frames[frame_id].data[other_frame_data]
                    scene.frames[frame_id].data[frame_data].uid = frame_data
                    break

    assert scene == scene_ground_truth


# Tests the warnings and errors
def test_no_warnings(openlabel_v1_short_data, loader):
    loader.load(openlabel_v1_short_data, validate=False)
    assert len(loader.warnings) == 0


def test_stream_with_no_coordinate_system(openlabel_v1_short_data, loader):
    del openlabel_v1_short_data["openlabel"]["coordinate_systems"]["ir_middle"]
    del openlabel_v1_short_data["openlabel"]["coordinate_systems"]["base"]["children"][
        openlabel_v1_short_data["openlabel"]["coordinate_systems"]["base"]["children"].index(
            "ir_middle"
        )
    ]
    with pytest.raises(raillabel.exceptions.MissingCoordinateSystemError):
        loader.load(openlabel_v1_short_data)


def test_warnings_sync(openlabel_v1_short_data, loader):
    openlabel_v1_short_data["openlabel"]["frames"]["0"]["frame_properties"]["streams"][
        "non_existing_stream"
    ] = {"stream_properties": {"sync": {"timestamp": "1632321743.100000072"}}}

    loader.load(openlabel_v1_short_data, validate=False)
    assert len(loader.warnings) == 1

    # Tests for keywords in the warning that can help the user identify the source
    assert "frame" in loader.warnings[0]
    assert "0" in loader.warnings[0]
    assert "sync" in loader.warnings[0]
    assert "non_existing_stream" in loader.warnings[0]


def test_warnings_stream_sync_field(openlabel_v1_short_data, loader):
    openlabel_v1_short_data["openlabel"]["frames"]["0"]["frame_properties"]["streams"][
        "rgb_middle"
    ]["stream_properties"]["stream_sync"] = openlabel_v1_short_data["openlabel"]["frames"]["0"][
        "frame_properties"
    ][
        "streams"
    ][
        "rgb_middle"
    ][
        "stream_properties"
    ][
        "sync"
    ]
    del openlabel_v1_short_data["openlabel"]["frames"]["0"]["frame_properties"]["streams"][
        "rgb_middle"
    ]["stream_properties"]["sync"]

    loader.load(openlabel_v1_short_data, validate=False)
    assert len(loader.warnings) == 1

    # Tests for keywords in the warning that can help the user identify the source
    assert "stream_sync" in loader.warnings[0]
    assert "deprecated" in loader.warnings[0].lower()
    assert "save()" in loader.warnings[0]


def test_warnings_ann_object(openlabel_v1_short_data, loader):
    openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "affeaffe-0327-46ff-9c28-2506cfd6d934"
    ] = {"object_data": {}}

    loader.load(openlabel_v1_short_data, validate=False)
    assert len(loader.warnings) == 1

    assert not "affeaffe-0327-46ff-9c28-2506cfd6d934" in loader.scene.frames[0].object_data

    # Tests for keywords in the warning that can help the user identify the source
    assert "frame" in loader.warnings[0]
    assert "0" in loader.warnings[0]
    assert "object" in loader.warnings[0]
    assert "affeaffe-0327-46ff-9c28-2506cfd6d934" in loader.warnings[0]


def test_warnings_wrong_annotation_cs(openlabel_v1_short_data, loader):
    openlabel_v1_short_data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["bbox"][0]["coordinate_system"] = "non_existent_sensor"

    loader.load(openlabel_v1_short_data, validate=False)
    assert len(loader.warnings) == 1

    assert (
        loader.scene.frames[0]
        .object_data["b40ba3ad-0327-46ff-9c28-2506cfd6d934"]
        .bboxs["78f0ad89-2750-4a30-9d66-44c9da73a714"]
        .sensor
        is None
    )

    # Tests for keywords in the warning that can help the user identify the source
    assert "annotation" in loader.warnings[0]
    assert "78f0ad89-2750-4a30-9d66-44c9da73a714" in loader.warnings[0]
    assert "sensor" in loader.warnings[0]
    assert "non_existent_sensor" in loader.warnings[0]


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
