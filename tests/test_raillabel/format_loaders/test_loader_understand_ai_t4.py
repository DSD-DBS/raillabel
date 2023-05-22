# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel


@pytest.fixture
def loader():
    return raillabel.format_loaders.LoaderUnderstandAiT4()


def test_supports_true(json_data, loader):
    assert loader.supports(json_data["understand_ai_real_life"])


def test_supports_false(json_data, loader):
    data = json_data["understand_ai_real_life"]
    data["metadata"]["project_id"] = "invalid"
    assert not loader.supports(data)


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
