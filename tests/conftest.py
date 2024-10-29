# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

import glob
import json
import sys
import typing as t
from pathlib import Path

import json5
import pytest

sys.path.insert(1, str(Path(__file__).parent.parent))
import raillabel

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
