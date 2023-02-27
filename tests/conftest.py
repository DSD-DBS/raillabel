# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
from pathlib import Path

import json5
import pytest

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
