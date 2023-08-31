# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import glob
import json
import sys
import typing as t
from pathlib import Path

import json5
import pytest

sys.path.insert(1, str(Path(__file__).parent.parent))

from test_raillabel.format.test_attributes import (
    attributes_multiple_types,
    attributes_multiple_types_dict,
    attributes_single_type,
    attributes_single_type_dict,
)
from test_raillabel.format.test_bbox import bbox, bbox_dict
from test_raillabel.format.test_cuboid import cuboid, cuboid_dict
from test_raillabel.format.test_element_data_pointer import (
    element_data_pointer_full,
    element_data_pointer_full_dict,
    element_data_pointer_minimal,
    element_data_pointer_minimal_dict,
)
from test_raillabel.format.test_frame import (
    frame_frame_data,
    frame_frame_data_dict,
    frame_sensors,
    frame_sensors_dict,
)
from test_raillabel.format.test_frame_interval import frame_interval, frame_interval_dict
from test_raillabel.format.test_intrinsics_pinhole import (
    intrinsics_pinhole,
    intrinsics_pinhole_dict,
)
from test_raillabel.format.test_intrinsics_radar import intrinsics_radar, intrinsics_radar_dict
from test_raillabel.format.test_metadata import (
    metadata_full,
    metadata_full_dict,
    metadata_minimal,
    metadata_minimal_dict,
)
from test_raillabel.format.test_num import num, num_dict
from test_raillabel.format.test_object import object_person, object_person_dict
from test_raillabel.format.test_object_data import object_data_person, object_data_person_dict
from test_raillabel.format.test_point2d import (
    point2d,
    point2d_another,
    point2d_another_dict,
    point2d_dict,
)
from test_raillabel.format.test_point3d import (
    point3d,
    point3d_another,
    point3d_another_dict,
    point3d_dict,
)
from test_raillabel.format.test_poly2d import poly2d, poly2d_dict
from test_raillabel.format.test_poly3d import poly3d, poly3d_dict
from test_raillabel.format.test_quaternion import quaternion, quaternion_dict
from test_raillabel.format.test_seg3d import seg3d, seg3d_dict
from test_raillabel.format.test_sensor import (
    sensor_camera,
    sensor_camera_dict,
    sensor_lidar,
    sensor_lidar_dict,
    sensor_radar,
    sensor_radar_dict,
)
from test_raillabel.format.test_sensor_reference import (
    sensor_reference_camera,
    sensor_reference_camera_dict,
)
from test_raillabel.format.test_size2d import size2d, size2d_dict
from test_raillabel.format.test_size3d import size3d, size3d_dict
from test_raillabel.format.test_transform import transform, transform_dict

import raillabel

json_data_directories = [
    Path(__file__).parent / "test_raillabel" / "__test_assets__",
    Path(__file__).parent.parent / "raillabel" / "schemas"
]

@pytest.fixture(scope="session", autouse=True)
def compile_uncommented_test_file():
    """Compiles the main test file from json5 to json."""

    json5_file_path = json_data_directories[0] / "openlabel_v1_short.json5"

    with json5_file_path.open() as f:
        data = json5.load(f)

    with open(str(json5_file_path)[:-1], "w") as f:
        json.dump(data, f, indent=4)

@pytest.fixture
def json_paths(request) -> t.Dict[str, Path]:
    json_paths = _fetch_json_paths_from_cache(request)

    if json_paths is None:
        json_paths = {_get_file_identifier(p): p for p in _collect_json_paths()}

    return json_paths

def _fetch_json_paths_from_cache(request) -> t.Optional[t.Dict[str, Path]]:
    return request.config.cache.get("json_paths", None)

def _collect_json_paths() -> t.List[Path]:
    json_paths = []

    for dir in json_data_directories:
        json_paths.extend([Path(p) for p in glob.glob(str(dir) + "/**/**.json", recursive=True)])

    return json_paths

def _get_file_identifier(path: Path) -> str:
    """Return relative path from test asset dir as string."""

    if "__test_assets__" not in path.parts:
        return path.stem

    test_assets_dir_index = path.parts.index("__test_assets__")

    relative_path = ""
    for part in path.parts[test_assets_dir_index+1:-1]:
        relative_path += part + "/"

    relative_path += path.stem

    return relative_path

@pytest.fixture
def json_data(request) -> t.Dict[str, dict]:
    json_data = _fetch_json_data_from_cache(request)

    if json_data is None:
        json_data = {_get_file_identifier(p): _load_json_data(p) for p in _collect_json_paths()}

    return json_data

def _fetch_json_data_from_cache(request) -> t.Optional[t.Dict[str, Path]]:
    return request.config.cache.get("json_data", None)

def _load_json_data(path: Path) -> dict:
    with path.open() as f:
        json_data = json.load(f)
    return json_data


@pytest.fixture
def annotation_compare_methods() -> t.Dict[str, t.Callable]:
    methods = {}

    def compare_bbox(annotation: raillabel.format.Bbox, ground_truth: dict) -> bool:

        assert type(annotation) == raillabel.format.Bbox
        assert annotation.uid == ground_truth["uid"]
        assert annotation.name == ground_truth["name"]
        assert annotation.pos.x == ground_truth["val"][0]
        assert annotation.pos.y == ground_truth["val"][1]
        assert annotation.size.x == ground_truth["val"][2]
        assert annotation.size.y == ground_truth["val"][3]

        if "coordinate_system" in ground_truth:
            assert annotation.sensor.uid == ground_truth["coordinate_system"]

        if "attributes" in ground_truth:

            accumulative_attributes = []
            for attr_type in ground_truth["attributes"].values():
                accumulative_attributes.extend(attr_type)

            assert len(annotation.attributes) == len(accumulative_attributes)
            for attribute in accumulative_attributes:
                assert attribute["name"] in annotation.attributes
                assert annotation.attributes[attribute["name"]] == attribute["val"]

    methods["bbox"] = compare_bbox


    def compare_cuboid(annotation: raillabel.format.Cuboid, ground_truth: dict) -> bool:

        assert type(annotation) == raillabel.format.Cuboid
        assert annotation.uid == ground_truth["uid"]
        assert annotation.name == ground_truth["name"]

        cuboid_val = [
            annotation.pos.x,
            annotation.pos.y,
            annotation.pos.z,
            annotation.quat.x,
            annotation.quat.y,
            annotation.quat.z,
            annotation.quat.w,
            annotation.size.x,
            annotation.size.y,
            annotation.size.z,
        ]
        assert cuboid_val == ground_truth["val"]

        if "coordinate_system" in ground_truth:
            assert annotation.sensor.uid == ground_truth["coordinate_system"]

        if "attributes" in ground_truth:

            accumulative_attributes = []
            for attr_type in ground_truth["attributes"].values():
                accumulative_attributes.extend(attr_type)

            assert len(annotation.attributes) == len(accumulative_attributes)
            for attribute in accumulative_attributes:
                assert attribute["name"] in annotation.attributes
                assert annotation.attributes[attribute["name"]] == attribute["val"]

    methods["cuboid"] = compare_cuboid


    def compare_num(annotation: raillabel.format.Num, ground_truth: dict) -> bool:

        assert type(annotation) == raillabel.format.Num
        assert annotation.uid == ground_truth["uid"]
        assert annotation.name == ground_truth["name"]
        assert annotation.val == ground_truth["val"]

        if "coordinate_system" in ground_truth:
            assert annotation.sensor.uid == ground_truth["coordinate_system"]

        if "attributes" in ground_truth:

            accumulative_attributes = []
            for attr_type in ground_truth["attributes"].values():
                accumulative_attributes.extend(attr_type)

            assert len(annotation.attributes) == len(accumulative_attributes)
            for attribute in accumulative_attributes:
                assert attribute["name"] in annotation.attributes
                assert annotation.attributes[attribute["name"]] == attribute["val"]

    methods["num"] = compare_num


    def compare_poly2d(annotation: raillabel.format.Poly2d, ground_truth: dict) -> bool:

        assert type(annotation) == raillabel.format.Poly2d
        assert annotation.uid == ground_truth["uid"]
        assert annotation.name == ground_truth["name"]

        for i in range(0, len(ground_truth["val"]), 2):
            assert annotation.points[i // 2].x == ground_truth["val"][i]
            assert annotation.points[i // 2].y == ground_truth["val"][i + 1]

        if "closed" in ground_truth:
            assert annotation.closed == ground_truth["closed"]

        if "mode" in ground_truth:
            assert annotation.mode == ground_truth["mode"]

        if "coordinate_system" in ground_truth:
            assert annotation.sensor.uid == ground_truth["coordinate_system"]

        if "attributes" in ground_truth:

            accumulative_attributes = []
            for attr_type in ground_truth["attributes"].values():
                accumulative_attributes.extend(attr_type)

            assert len(annotation.attributes) == len(accumulative_attributes)
            for attribute in accumulative_attributes:
                assert attribute["name"] in annotation.attributes
                assert annotation.attributes[attribute["name"]] == attribute["val"]

    methods["poly2d"] = compare_poly2d


    def compare_poly3d(annotation: raillabel.format.Poly3d, ground_truth: dict) -> bool:

        assert type(annotation) == raillabel.format.Poly3d
        assert annotation.uid == ground_truth["uid"]
        assert annotation.name == ground_truth["name"]

        for i in range(0, len(ground_truth["val"]), 3):
            assert annotation.points[int(i / 3)].x == ground_truth["val"][i]
            assert annotation.points[int(i / 3)].y == ground_truth["val"][i + 1]
            assert annotation.points[int(i / 3)].z == ground_truth["val"][i + 2]

        if "closed" in ground_truth:
            assert annotation.closed == ground_truth["closed"]

        if "coordinate_system" in ground_truth:
            assert annotation.sensor.uid == ground_truth["coordinate_system"]

        if "attributes" in ground_truth:

            accumulative_attributes = []
            for attr_type in ground_truth["attributes"].values():
                accumulative_attributes.extend(attr_type)

            assert len(annotation.attributes) == len(accumulative_attributes)
            for attribute in accumulative_attributes:
                assert attribute["name"] in annotation.attributes
                assert annotation.attributes[attribute["name"]] == attribute["val"]

    methods["poly3d"] = compare_poly3d


    def compare_seg3d(annotation: raillabel.format.Seg3d, ground_truth: dict) -> bool:

        assert type(annotation) == raillabel.format.Seg3d
        assert annotation.uid == ground_truth["uid"]
        assert annotation.name == ground_truth["name"]
        assert annotation.point_ids == ground_truth["val"]

        if "coordinate_system" in ground_truth:
            assert annotation.sensor.uid == ground_truth["coordinate_system"]

        if "attributes" in ground_truth:

            accumulative_attributes = []
            for attr_type in ground_truth["attributes"].values():
                accumulative_attributes.extend(attr_type)

            assert len(annotation.attributes) == len(accumulative_attributes)
            for attribute in accumulative_attributes:
                assert attribute["name"] in annotation.attributes
                assert annotation.attributes[attribute["name"]] == attribute["val"]

    methods["vec"] = compare_seg3d

    return methods
