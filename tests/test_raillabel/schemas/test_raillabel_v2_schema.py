# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os

import jsonschema
import pytest


def test_metaschema_validation(raillabel_v2_schema_data, metaschema_data):
    assert jsonschema.validate(raillabel_v2_schema_data, metaschema_data) is None


def test_sample_data_validation_subschema(raillabel_v2_schema_data, openlabel_v1_short_data):
    assert jsonschema.validate(openlabel_v1_short_data, raillabel_v2_schema_data) is None


def test_sample_data_validation_superschema(openlabel_v1_schema_data, openlabel_v1_short_data):
    assert jsonschema.validate(openlabel_v1_short_data, openlabel_v1_schema_data) is None


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
