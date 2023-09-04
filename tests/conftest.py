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

from test_raillabel.format.raillabel.test_attributes import (
    attributes_multiple_types,
    attributes_multiple_types_dict,
    attributes_single_type,
    attributes_single_type_dict,
)
from test_raillabel.format.raillabel.test_bbox import bbox, bbox_dict, bbox_train, bbox_train_dict
from test_raillabel.format.raillabel.test_cuboid import cuboid, cuboid_dict
from test_raillabel.format.raillabel.test_element_data_pointer import (
    element_data_pointer_full,
    element_data_pointer_full_dict,
    element_data_pointer_minimal,
    element_data_pointer_minimal_dict,
)
from test_raillabel.format.raillabel.test_frame import frame, frame_dict
from test_raillabel.format.raillabel.test_frame_interval import frame_interval, frame_interval_dict
from test_raillabel.format.raillabel.test_intrinsics_pinhole import (
    intrinsics_pinhole,
    intrinsics_pinhole_dict,
)
from test_raillabel.format.raillabel.test_intrinsics_radar import (
    intrinsics_radar,
    intrinsics_radar_dict,
)
from test_raillabel.format.raillabel.test_metadata import (
    metadata_full,
    metadata_full_dict,
    metadata_minimal,
    metadata_minimal_dict,
)
from test_raillabel.format.raillabel.test_num import num, num_dict
from test_raillabel.format.raillabel.test_object import (
    object_person,
    object_person_dict,
    object_train,
    object_train_dict,
    objects,
    objects_dict,
)
from test_raillabel.format.raillabel.test_object_annotation import all_annotations
from test_raillabel.format.raillabel.test_object_data import (
    object_data_person_dict,
    object_data_train_dict,
)
from test_raillabel.format.raillabel.test_point2d import (
    point2d,
    point2d_another,
    point2d_another_dict,
    point2d_dict,
)
from test_raillabel.format.raillabel.test_point3d import (
    point3d,
    point3d_another,
    point3d_another_dict,
    point3d_dict,
)
from test_raillabel.format.raillabel.test_poly2d import poly2d, poly2d_dict
from test_raillabel.format.raillabel.test_poly3d import poly3d, poly3d_dict
from test_raillabel.format.raillabel.test_quaternion import quaternion, quaternion_dict
from test_raillabel.format.raillabel.test_scene import scene, scene_dict
from test_raillabel.format.raillabel.test_seg3d import seg3d, seg3d_dict
from test_raillabel.format.raillabel.test_sensor import (
    coordinate_systems_dict,
    sensor_camera,
    sensor_camera_dict,
    sensor_lidar,
    sensor_lidar_dict,
    sensor_radar,
    sensor_radar_dict,
    sensors,
    streams_dict,
)
from test_raillabel.format.raillabel.test_sensor_reference import (
    sensor_reference_camera,
    sensor_reference_camera_dict,
)
from test_raillabel.format.raillabel.test_size2d import size2d, size2d_dict
from test_raillabel.format.raillabel.test_size3d import size3d, size3d_dict
from test_raillabel.format.raillabel.test_transform import transform, transform_dict

import raillabel

json_data_directories = [
    Path(__file__).parent / "__test_assets__",
    Path(__file__).parent.parent / "raillabel" / "validate" / "schemas"
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
