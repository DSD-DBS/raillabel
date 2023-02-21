# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

import raillabel


def test_valid_file(openlabel_v1_short_data):
    validation_result = raillabel.validate(openlabel_v1_short_data)
    assert validation_result[0]


def test_file_one_type_error(openlabel_v1_short_data):
    openlabel_v1_short_data["openlabel"]["streams"]["lidar"]["uri"] = 42

    validation_result = raillabel.validate(openlabel_v1_short_data)

    assert not validation_result[0] and len(validation_result[1]) == 1


def test_file_two_type_errors(openlabel_v1_short_data):
    openlabel_v1_short_data["openlabel"]["streams"]["lidar"]["uri"] = 42
    openlabel_v1_short_data["openlabel"]["coordinate_systems"]["base"]["type"] = "invalid_value"

    validation_result = raillabel.validate(openlabel_v1_short_data)

    assert not validation_result[0] and len(validation_result[1]) == 2


def test_valid_file_path(openlabel_v1_short_data, raillabel_v2_schema_path):
    assert raillabel_v2_schema_path.is_file()
    validation_result = raillabel.validate(openlabel_v1_short_data, str(raillabel_v2_schema_path))
    assert validation_result[0]


def test_invalid_file_path(openlabel_v1_short_data, raillabel_v2_schema_path):
    raillabel_v2_schema_path = str(raillabel_v2_schema_path) + "_invalid"

    with pytest.raises(FileNotFoundError):
        raillabel.validate(openlabel_v1_short_data, raillabel_v2_schema_path)


def test_invalid_schema_key(openlabel_v1_short_data):
    with pytest.raises(FileNotFoundError):
        raillabel.validate(openlabel_v1_short_data, "invalid_schema")


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
