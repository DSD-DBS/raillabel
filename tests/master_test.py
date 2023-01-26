# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import pathlib

import pytest

# Executes the test
pytest.main(
    [
        str(pathlib.Path(__file__).parent),
        "--disable-pytest-warnings",
        "--cache-clear",
    ]
)
