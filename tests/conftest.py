# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import glob
import json
import sys
import typing as t
from pathlib import Path

import json5
import pytest

sys.path.insert(1, str(Path(__file__).parent.parent))
import raillabel


from format.test_attributes import attributes_multiple_types, attributes_multiple_types_json
from format.test_bbox import bbox, bbox_json, bbox_id
from format.test_camera import camera, camera_json, camera_empty
from format.test_cuboid import cuboid, cuboid_json, cuboid_id
from format.test_frame import frame, frame_json
from format.test_frame_interval import frame_interval, frame_interval_json
from format.test_intrinsics_pinhole import intrinsics_pinhole, intrinsics_pinhole_json
from format.test_intrinsics_radar import intrinsics_radar, intrinsics_radar_json
from format.test_lidar import lidar, lidar_json
from format.test_metadata import metadata, metadata_json
from format.test_num import num, num_json, num_id
from format.test_object import (
    objects,
    object_person,
    object_person_json,
    object_person_id,
    object_track,
    object_track_json,
    object_track_id,
)
from format.test_point2d import point2d, point2d_json, another_point2d, another_point2d_json
from format.test_point3d import point3d, point3d_json, another_point3d, another_point3d_json
from format.test_poly2d import poly2d, poly2d_json, poly2d_id
from format.test_poly3d import poly3d, poly3d_json, poly3d_id
from format.test_quaternion import quaternion, quaternion_json
from format.test_radar import radar, radar_json, radar_empty
from format.test_size2d import size2d, size2d_json
from format.test_size3d import size3d, size3d_json
from format.test_seg3d import seg3d, seg3d_json, seg3d_id
from format.test_sensor_reference import (
    another_sensor_reference,
    another_sensor_reference_json,
    sensor_reference,
    sensor_reference_json,
)
from format.test_transform import transform, transform_json


json_data_directories = [
    Path(__file__).parent / "__test_assets__",
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
def json_paths(request) -> dict[str, Path]:
    json_paths = _fetch_json_paths_from_cache(request)

    if json_paths is None:
        json_paths = {_get_file_identifier(p): p for p in _collect_json_paths()}

    return json_paths


def _fetch_json_paths_from_cache(request) -> dict[str, Path] | None:
    return request.config.cache.get("json_paths", None)


def _collect_json_paths() -> list[Path]:
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
    for part in path.parts[test_assets_dir_index + 1 : -1]:
        relative_path += part + "/"

    relative_path += path.stem

    return relative_path


@pytest.fixture
def json_data(request) -> dict[str, dict]:
    json_data = _fetch_json_data_from_cache(request)

    if json_data is None:
        json_data = {_get_file_identifier(p): _load_json_data(p) for p in _collect_json_paths()}

    return json_data


def _fetch_json_data_from_cache(request) -> dict[str, Path] | None:
    return request.config.cache.get("json_data", None)


def _load_json_data(path: Path) -> dict:
    with path.open() as f:
        json_data = json.load(f)
    return json_data
