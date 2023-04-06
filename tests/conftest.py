# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
import sys
import typing as t
from pathlib import Path

import json5
import pytest

sys.path.insert(1, str(Path(__file__).parent.parent))

import raillabel

# Variables
raillabel_v2_schema_path_var = (
    Path(__file__).parent.parent / "raillabel" / "schemas" / "raillabel_v2_schema.json"
)
metaschema_path_var = (
    Path(__file__).parent / "test_raillabel" / "__test_assets__" / "metaschema.json"
)
openlabel_v1_schema_path_var = (
    Path(__file__).parent / "test_raillabel" / "__test_assets__" / "openlabel_v1_schema.json"
)
openlabel_v1_short_path_var = (
    Path(__file__).parent / "test_raillabel" / "__test_assets__" / "openlabel_v1_short.json"
)
openlabel_v1_vcd_incompatible_path_var = (
    Path(__file__).parent
    / "test_raillabel"
    / "__test_assets__"
    / "openlabel_v1_vcd_incompatible.json"
)


@pytest.fixture(scope="session", autouse=True)
def compile_uncommented_test_file():
    """Compiles the main test file from json5 to json."""

    uncommented_example_file_path = Path(str(openlabel_v1_short_path_var) + "5")

    with uncommented_example_file_path.open() as f:
        data = json5.load(f)

    with openlabel_v1_short_path_var.open("w") as f:
        json.dump(data, f, indent=4)


# Raillabel v2 schema
@pytest.fixture
def raillabel_v2_schema_path():
    return raillabel_v2_schema_path_var


@pytest.fixture
def raillabel_v2_schema_data(request):
    raillabel_v2_schema_data = request.config.cache.get("raillabel_v2_schema_data", None)

    if raillabel_v2_schema_data is None:
        with raillabel_v2_schema_path_var.open() as raillabel_v2_short_file:
            raillabel_v2_schema_data = json.load(raillabel_v2_short_file)
            request.config.cache.set("raillabel_v2_schema_data", raillabel_v2_schema_data)

    return raillabel_v2_schema_data


# JSON metaschema
@pytest.fixture
def metaschema_path():
    return metaschema_path_var


@pytest.fixture
def metaschema_data(request):
    metaschema_data = request.config.cache.get("metaschema_data", None)

    if metaschema_data is None:
        with metaschema_path_var.open() as metashort_file:
            metaschema_data = json.load(metashort_file)
            request.config.cache.set("metaschema_data", metaschema_data)

    return metaschema_data


# JSON openlabel_v1_schema
@pytest.fixture
def openlabel_v1_schema_path():
    return openlabel_v1_schema_path_var


@pytest.fixture
def openlabel_v1_schema_data(request):
    openlabel_v1_schema_data = request.config.cache.get("openlabel_v1_schema_data", None)

    if openlabel_v1_schema_data is None:
        with openlabel_v1_schema_path_var.open() as openlabel_v1_short_file:
            openlabel_v1_schema_data = json.load(openlabel_v1_short_file)
            request.config.cache.set("openlabel_v1_schema_data", openlabel_v1_schema_data)

    return openlabel_v1_schema_data


# OpenLabel v1 short data
@pytest.fixture
def openlabel_v1_short_path():
    return openlabel_v1_short_path_var


@pytest.fixture
def openlabel_v1_short_data(request):
    openlabel_v1_short_data = request.config.cache.get("openlabel_v1_short_data", None)

    if openlabel_v1_short_data is None:
        with openlabel_v1_short_path_var.open() as openlabel_v1_short_file:
            openlabel_v1_short_data = json5.load(openlabel_v1_short_file)
            request.config.cache.set("openlabel_v1_short_data", openlabel_v1_short_data)

    return openlabel_v1_short_data


# OpenLabel v1 short vcd incompatible
@pytest.fixture
def openlabel_v1_vcd_incompatible_path():
    return openlabel_v1_vcd_incompatible_path_var


@pytest.fixture
def openlabel_v1_vcd_incompatible_data(request):
    openlabel_v1_vcd_incompatible_data = request.config.cache.get(
        "openlabel_v1_vcd_incompatible_data", None
    )

    if openlabel_v1_vcd_incompatible_data is None:
        with openlabel_v1_vcd_incompatible_path_var.open() as openlabel_v1_vcd_incompatible_file:
            openlabel_v1_vcd_incompatible_data = json.load(openlabel_v1_vcd_incompatible_file)
            request.config.cache.set(
                "openlabel_v1_vcd_incompatible_data",
                openlabel_v1_vcd_incompatible_data,
            )

    return openlabel_v1_vcd_incompatible_data

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
        assert annotation.pos.x == ground_truth["val"][0]
        assert annotation.pos.y == ground_truth["val"][1]
        assert annotation.pos.z == ground_truth["val"][2]
        assert annotation.quat.x == ground_truth["val"][3]
        assert annotation.quat.y == ground_truth["val"][4]
        assert annotation.quat.z == ground_truth["val"][5]
        assert annotation.quat.w == ground_truth["val"][6]
        assert annotation.size.x == ground_truth["val"][7]
        assert annotation.size.y == ground_truth["val"][8]
        assert annotation.size.z == ground_truth["val"][9]

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
            assert annotation.points[int(i / 2)].x == ground_truth["val"][i]
            assert annotation.points[int(i / 2)].y == ground_truth["val"][i + 1]

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
