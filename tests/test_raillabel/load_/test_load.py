# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel


def test_load_raillabel(json_paths):
    data_path = json_paths["openlabel_v1_short"]
    scene = raillabel.load(data_path)
    assert len(scene.frames) != 0


def test_load_uai(json_paths):
    data_path = json_paths["understand_ai_t4_short"]
    scene = raillabel.load(data_path)
    assert len(scene.frames) != 0


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
