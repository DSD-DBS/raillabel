# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
import pathlib

import pytest

# Variables
openlabel_v1_schema_path_var = (
    pathlib.Path(__file__).parent.parent / "raillabel" / "schemas" / "openlabel_v1_schema.json"
)
openlabel_v1_short_path_var = (
    pathlib.Path(__file__).parent / "test_raillabel" / "__test_assets__" / "openlabel_v1_short.json"
)
openlabel_v1_vcd_incompatible_path_var = (
    pathlib.Path(__file__).parent
    / "test_raillabel"
    / "__test_assets__"
    / "openlabel_v1_vcd_incompatible.json"
)
understandai_v3_schema_path_var = (
    pathlib.Path(__file__).parent.parent / "raillabel" / "schemas" / "understandai_v3_schema.json"
)
understandai_v3_short_path_var = (
    pathlib.Path(__file__).parent
    / "test_raillabel"
    / "__test_assets__"
    / "understandai_v3_short.json"
)
clabel_v2_schema_path_var = (
    pathlib.Path(__file__).parent.parent / "raillabel" / "schemas" / "clabel_v2_schema.json"
)
clabel_v2_short_path_var = (
    pathlib.Path(__file__).parent / "test_raillabel" / "__test_assets__" / "clabel_v2_short.json"
)

# OpenLabel v1 schema
@pytest.fixture
def openlabel_v1_schema_path():
    return openlabel_v1_short_path_var


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
            openlabel_v1_short_data = json.load(openlabel_v1_short_file)
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


# UnderstandAi v3 schema
@pytest.fixture
def understandai_v3_schema_path():
    return understandai_v3_short_path_var


@pytest.fixture
def understandai_v3_schema_data(request):
    understandai_v3_schema_data = request.config.cache.get("understandai_v3_schema_data", None)

    if understandai_v3_schema_data is None:
        with understandai_v3_schema_path_var.open() as understandai_v3_short_file:
            understandai_v3_schema_data = json.load(understandai_v3_short_file)
            request.config.cache.set("understandai_v3_schema_data", understandai_v3_schema_data)

    return understandai_v3_schema_data


# UnderstandAi v3 short data
@pytest.fixture
def understandai_v3_short_path():
    return understandai_v3_short_path_var


@pytest.fixture
def understandai_v3_short_data(request):
    understandai_v3_short_data = request.config.cache.get("understandai_v3_short_data", None)

    if understandai_v3_short_data is None:
        with understandai_v3_short_path_var.open() as understandai_v3_short_file:
            understandai_v3_short_data = json.load(understandai_v3_short_file)
            request.config.cache.set("understandai_v3_short_data", understandai_v3_short_data)

    return understandai_v3_short_data


# C.LABEL v2 schema
@pytest.fixture
def clabel_v2_schema_path():
    return clabel_v2_short_path_var


@pytest.fixture
def clabel_v2_schema_data(request):
    clabel_v2_schema_data = request.config.cache.get("clabel_v2_schema_data", None)

    if clabel_v2_schema_data is None:
        with clabel_v2_schema_path_var.open() as clabel_v2_short_file:
            clabel_v2_schema_data = json.load(clabel_v2_short_file)
            request.config.cache.set("clabel_v2_schema_data", clabel_v2_schema_data)

    return clabel_v2_schema_data


# C.LABEL v2 short data
@pytest.fixture
def clabel_v2_short_path():
    return clabel_v2_short_path_var


@pytest.fixture
def clabel_v2_short_data(request):
    clabel_v2_short_data = request.config.cache.get("clabel_v2_short_data", None)

    if clabel_v2_short_data is None:
        with clabel_v2_short_path_var.open() as clabel_v2_short_file:
            clabel_v2_short_data = json.load(clabel_v2_short_file)
            request.config.cache.set("clabel_v2_short_data", clabel_v2_short_data)

    return clabel_v2_short_data
