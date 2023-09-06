# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Transform

# == Fixtures =========================

@pytest.fixture
def transform_dict(point3d_dict, quaternion_dict) -> dict:
    return {
        "translation": point3d_dict,
        "quaternion": quaternion_dict
    }

@pytest.fixture
def transform(point3d, quaternion) -> dict:
    return Transform(
        pos=point3d,
        quat=quaternion
    )

# == Tests ============================

def test_fromdict(point3d, point3d_dict, quaternion, quaternion_dict):
    transform = Transform.fromdict(
        {
            "translation": point3d_dict,
            "quaternion": quaternion_dict
        }
    )

    assert transform.pos == point3d
    assert transform.quat == quaternion


def test_asdict(point3d, point3d_dict, quaternion, quaternion_dict):
    transform = Transform(
        pos=point3d,
        quat=quaternion
    )

    assert transform.asdict() == {
        "translation": point3d_dict,
        "quaternion": quaternion_dict
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
