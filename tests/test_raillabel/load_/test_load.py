# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os

import pytest

import raillabel


def test_load__contains_all_elements(json_paths):
    actual = raillabel.load(json_paths["openlabel_v1_short"])
    assert len(actual.sensors) == 4
    assert len(actual.objects) == 3
    assert len(actual.frames) == 2


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
