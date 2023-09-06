# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

import raillabel.format.understand_ai as uai_format

# == Fixtures =========================

@pytest.fixture
def size_3d_uai_dict() -> dict:
    return {
        "width": 3,
        "length": 4,
        "height": 5,
    }

@pytest.fixture
def size_3d_uai() -> dict:
    return uai_format.Size3d(
        width=3,
        length=4,
        height=5,
    )

@pytest.fixture
def size_3d_vec() -> dict:
    return [3, 4, 5]

# == Tests ============================

def test_fromdict():
    size_3d = uai_format.Size3d.fromdict(
        {
            "width": 3,
            "length": 4,
            "height": 5,
        }
    )

    assert size_3d.width == 3
    assert size_3d.length == 4
    assert size_3d.height == 5


if __name__ == "__main__":
    import os
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
