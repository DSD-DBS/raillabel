# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel


@pytest.fixture
def loader():
    return raillabel.format_loaders.LoaderRailLabelV2()


def test_supports_true(json_data, loader):
    assert loader.supports(json_data["openlabel_v1_short"])


def test_supports_false(json_data, loader):
    data = json_data["openlabel_v1_short"]
    data["openlabel"]["metadata"]["subschema_version"] = "3.0.0"
    assert not loader.supports(data)


def test_load_metadata(json_data, loader):
    scene = loader.load(json_data["openlabel_v1_short"], validate=False)

    ground_truth = json_data["openlabel_v1_short"]["openlabel"]

    assert scene.metadata.annotator == ground_truth["metadata"]["annotator"]
    assert scene.metadata.comment == ground_truth["metadata"]["comment"]
    assert scene.metadata.name == ground_truth["metadata"]["name"]
    assert scene.metadata.schema_version == ground_truth["metadata"]["schema_version"]
    assert scene.metadata.tagged_file == ground_truth["metadata"]["tagged_file"]
    assert scene.metadata.subschema_version == json_data["raillabel_v2_schema"]["version"]


def test_load_sensors(json_data, loader):
    scene = loader.load(json_data["openlabel_v1_short"], validate=False)

    ground_truth = json_data["openlabel_v1_short"]["openlabel"]

    assert len(scene.sensors) == len(ground_truth["streams"])
    for sensor_id, sensor in scene.sensors.items():

        assert sensor_id in ground_truth["streams"]
        assert sensor.uid == sensor_id
        assert sensor.type.value == ground_truth["streams"][sensor_id]["type"]
        assert sensor.uri == ground_truth["streams"][sensor_id]["uri"]

        assert [
            sensor.extrinsics.pos.x,
            sensor.extrinsics.pos.y,
            sensor.extrinsics.pos.z,
        ] == ground_truth["coordinate_systems"][sensor_id]["pose_wrt_parent"]["translation"]
        assert [
            sensor.extrinsics.quat.x,
            sensor.extrinsics.quat.y,
            sensor.extrinsics.quat.z,
            sensor.extrinsics.quat.w,
        ] == ground_truth["coordinate_systems"][sensor_id]["pose_wrt_parent"]["quaternion"]

        if sensor.type.value != "camera":
            continue

        assert list(sensor.intrinsics.camera_matrix) == ground_truth["streams"][sensor_id]["stream_properties"]["intrinsics_pinhole"]["camera_matrix"]
        assert list(sensor.intrinsics.distortion) == ground_truth["streams"][sensor_id]["stream_properties"]["intrinsics_pinhole"]["distortion_coeffs"]
        assert sensor.intrinsics.width_px == ground_truth["streams"][sensor_id]["stream_properties"]["intrinsics_pinhole"]["width_px"]
        assert sensor.intrinsics.height_px == ground_truth["streams"][sensor_id]["stream_properties"]["intrinsics_pinhole"]["height_px"]


def test_load_objects(json_data, loader):
    scene = loader.load(json_data["openlabel_v1_short"], validate=False)

    ground_truth = json_data["openlabel_v1_short"]["openlabel"]

    assert len(scene.objects) == len(ground_truth["objects"])
    for object_id, object in scene.objects.items():

        assert object_id in ground_truth["objects"]
        assert object.uid == object_id
        assert object.name == ground_truth["objects"][object_id]["name"]
        assert object.type == ground_truth["objects"][object_id]["type"]


def test_load_frames_completeness(json_data, loader):
    scene = loader.load(json_data["openlabel_v1_short"], validate=False)

    ground_truth = json_data["openlabel_v1_short"]["openlabel"]

    assert len(scene.frames) == len(ground_truth["frames"])
    for frame_id, frame in scene.frames.items():

        assert str(frame_id) in ground_truth["frames"]
        assert frame.uid == frame_id


def test_load_frame_timestamps(json_data, loader):
    scene = loader.load(json_data["openlabel_v1_short"], validate=False)

    ground_truth = json_data["openlabel_v1_short"]["openlabel"]

    for frame_id, frame in scene.frames.items():
        assert str(frame.timestamp) == ground_truth["frames"][str(frame_id)]["frame_properties"]["timestamp"]


def test_load_frame_sensors(json_data, loader):
    scene = loader.load(json_data["openlabel_v1_short"], validate=False)

    ground_truth = json_data["openlabel_v1_short"]["openlabel"]

    for frame_id, frame in scene.frames.items():

        assert len(frame.sensors) == len(ground_truth["frames"][str(frame_id)]["frame_properties"]["streams"])
        for sensor_id, sensor in frame.sensors.items():

            assert sensor_id in ground_truth["frames"][str(frame_id)]["frame_properties"]["streams"]
            assert str(sensor.timestamp) == ground_truth["frames"][str(frame_id)]["frame_properties"]["streams"][sensor_id]["stream_properties"]["sync"]["timestamp"]
            assert str(sensor.uri) == ground_truth["frames"][str(frame_id)]["frame_properties"]["streams"][sensor_id]["uri"]


def test_load_frame_data(json_data, loader, annotation_compare_methods):
    scene = loader.load(json_data["openlabel_v1_short"], validate=False)

    ground_truth = json_data["openlabel_v1_short"]["openlabel"]

    for frame_id, frame in scene.frames.items():

        accumulative_frame_data = []
        for frame_data_type in ground_truth["frames"][str(frame_id)]["frame_properties"]["frame_data"].values():
            accumulative_frame_data.extend(frame_data_type)

        assert len(frame.data) == len(accumulative_frame_data)

        for frame_data_type, frame_data in ground_truth["frames"][str(frame_id)]["frame_properties"]["frame_data"].items():
            for annotation in frame_data:
                annotation_compare_methods[frame_data_type](frame.data[annotation["name"]], annotation)


def test_load_frame_annotations(json_data, loader, annotation_compare_methods):
    scene = loader.load(json_data["openlabel_v1_short"], validate=False)

    ground_truth = json_data["openlabel_v1_short"]["openlabel"]

    for frame_id, frame in scene.frames.items():

        assert len(frame.object_data) == len(ground_truth["frames"][str(frame_id)]["objects"])
        for object_id, object_data in ground_truth["frames"][str(frame_id)]["objects"].items():
            assert object_id in frame.object_data

            object_data = object_data["object_data"]

            accumulative_object_data = []
            for object_data_type in object_data.values():
                accumulative_object_data.extend(object_data_type)

            assert len(frame.object_data[object_id].annotations) == len(accumulative_object_data)

            for object_data_type, object_data in object_data.items():
                for annotation in object_data:
                    annotation_compare_methods[object_data_type](frame.annotations[annotation["uid"]], annotation)


def test_load_uri_vcd_incompatible(
    json_data, loader
):
    """Tests, whether an older annotation file, which is not usable for the VCD
    library is converted into a compatible one."""

    scene_ground_truth = loader.load(json_data["openlabel_v1_short"], validate=False)
    scene = loader.load(
        json_data["openlabel_v1_vcd_incompatible"],
        validate=False
    )

    # The UUIDs of the frame data have been generated and therefore do not match the ground truth.
    # They are set equal here.
    for frame_id in scene_ground_truth.frames:
        for frame_data in scene_ground_truth.frames[frame_id].data:
            scene.frames[frame_id].data[frame_data].uid = (
                scene_ground_truth.frames[frame_id].data[frame_data].uid
            )

    assert scene == scene_ground_truth


# Tests the warnings and errors
def test_no_warnings(json_data, loader):
    loader.load(json_data["openlabel_v1_short"], validate=False)
    assert len(loader.warnings) == 0


def test_warning_uri_attribute(
    json_data, loader
):

    loader.load(
        json_data["openlabel_v1_vcd_incompatible"],
        validate=False
    )

    assert "attribute" in loader.warnings[0]
    assert "uri" in loader.warnings[0]


def test_stream_with_no_coordinate_system(json_data, loader):
    data = json_data["openlabel_v1_short"]

    del data["openlabel"]["coordinate_systems"]["ir_middle"]
    del data["openlabel"]["coordinate_systems"]["base"]["children"][
        data["openlabel"]["coordinate_systems"]["base"]["children"].index(
            "ir_middle"
        )
    ]
    with pytest.raises(raillabel.exceptions.MissingCoordinateSystemError):
        loader.load(data)


def test_warnings_sync(json_data, loader):
    data = json_data["openlabel_v1_short"]

    data["openlabel"]["frames"]["0"]["frame_properties"]["streams"]["non_existing_stream"] = {
        "stream_properties": {
            "sync": {
                "timestamp": "1632321743.100000072"
            }
        }
    }

    loader.load(data, validate=False)
    assert len(loader.warnings) == 1

    # Tests for keywords in the warning that can help the user identify the source
    assert "frame" in loader.warnings[0]
    assert "0" in loader.warnings[0]
    assert "sync" in loader.warnings[0]
    assert "non_existing_stream" in loader.warnings[0]


def test_warnings_stream_sync_field(json_data, loader):
    data = json_data["openlabel_v1_short"]

    data["openlabel"]["frames"]["0"]["frame_properties"]["streams"][
        "rgb_middle"
    ]["stream_properties"]["stream_sync"] = data["openlabel"]["frames"]["0"][
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
    del data["openlabel"]["frames"]["0"]["frame_properties"]["streams"][
        "rgb_middle"
    ]["stream_properties"]["sync"]

    loader.load(data, validate=False)
    assert len(loader.warnings) == 1

    # Tests for keywords in the warning that can help the user identify the source
    assert "stream_sync" in loader.warnings[0]
    assert "deprecated" in loader.warnings[0].lower()
    assert "save()" in loader.warnings[0]


def test_warnings_ann_object(json_data, loader):
    data = json_data["openlabel_v1_short"]

    data["openlabel"]["frames"]["0"]["objects"][
        "affeaffe-0327-46ff-9c28-2506cfd6d934"
    ] = {"object_data": {}}

    loader.load(data, validate=False)
    assert len(loader.warnings) == 1

    assert not "affeaffe-0327-46ff-9c28-2506cfd6d934" in loader.scene.frames[0].object_data

    # Tests for keywords in the warning that can help the user identify the source
    assert "frame" in loader.warnings[0]
    assert "0" in loader.warnings[0]
    assert "object" in loader.warnings[0]
    assert "affeaffe-0327-46ff-9c28-2506cfd6d934" in loader.warnings[0]


def test_warnings_wrong_annotation_cs(json_data, loader):
    data = json_data["openlabel_v1_short"]

    data["openlabel"]["frames"]["0"]["objects"][
        "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    ]["object_data"]["bbox"][0]["coordinate_system"] = "non_existent_sensor"

    loader.load(data, validate=False)
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


def test_identify_of_references(json_data, loader):
    data = json_data["openlabel_v1_short"]

    scene = loader.load(data, validate=False)

    for frame in scene.frames.values():

        for sensor_reference in frame.sensors.values():
            assert sensor_reference.sensor is scene.sensors[sensor_reference.sensor.uid]

        for frame_data in frame.data.values():
            assert frame_data.sensor is scene.sensors[frame_data.sensor.uid]

        for annotation in frame.annotations.values():
            assert annotation.sensor is scene.sensors[annotation.sensor.uid]


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
