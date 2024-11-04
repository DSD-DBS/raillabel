# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os

import pytest

from raillabel.json_format import JSONScene


def test_parse__openlabel_short(json_data):
    JSONScene(**json_data["openlabel_v1_short"])


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
