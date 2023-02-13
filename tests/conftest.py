# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
import pathlib

import pytest

# Variables
raillabel_v2_schema_path_var = (
    pathlib.Path(__file__).parent.parent / "raillabel" / "schemas" / "raillabel_v2_schema.json"
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

# OpenLabel v1 schema
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
