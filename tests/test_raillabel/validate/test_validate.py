# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel


def test_valid_file(json_data):
    validation_result = raillabel.validate(json_data["openlabel_v1_short"])
    assert validation_result[0]


def test_file_one_type_error(json_data):
    data = json_data["openlabel_v1_short"]

    data["openlabel"]["streams"]["lidar"]["uri"] = 42

    validation_result = raillabel.validate(data)

    assert not validation_result[0] and len(validation_result[1]) == 1


def test_file_two_type_errors(json_data):
    data = json_data["openlabel_v1_short"]

    data["openlabel"]["streams"]["lidar"]["uri"] = 42
    data["openlabel"]["coordinate_systems"]["base"]["type"] = "invalid_value"

    validation_result = raillabel.validate(data)

    assert not validation_result[0] and len(validation_result[1]) == 2


def test_valid_file_path(json_data, json_paths):
    validation_result = raillabel.validate(json_data["openlabel_v1_short"], str(json_paths["raillabel_schema"]))
    assert validation_result[0]


def test_invalid_file_path(json_data, json_paths):
    json_paths["raillabel_schema"] = str(json_paths["raillabel_schema"]) + "_invalid"

    with pytest.raises(FileNotFoundError):
        raillabel.validate(json_data["openlabel_v1_short"], json_paths["raillabel_schema"])


def test_invalid_schema_key(json_data):
    with pytest.raises(FileNotFoundError):
        raillabel.validate(json_data["openlabel_v1_short"], "invalid_schema")


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
