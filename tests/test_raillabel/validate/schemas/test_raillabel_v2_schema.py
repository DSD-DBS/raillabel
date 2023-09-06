# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os

import jsonschema
import pytest


def test_metaschema_validation(json_data):
    assert jsonschema.validate(
        json_data["raillabel_schema"],
        json_data["metaschema"]
    ) is None


def test_sample_data_validation_subschema(json_data):
    assert jsonschema.validate(
        json_data["openlabel_v1_short"],
        json_data["raillabel_schema"]
    ) is None


def test_sample_data_validation_superschema(json_data):
    assert jsonschema.validate(
        json_data["openlabel_v1_short"],
        json_data["openlabel_v1_schema"]
    ) is None


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
