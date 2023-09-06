# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

# == Fixtures =========================

@pytest.fixture
def object_data_person_dict(bbox_dict, poly2d_dict, cuboid_dict, poly3d_dict, seg3d_dict) -> dict:
    return {
        "object_data": {
            "bbox": [bbox_dict],
            "poly2d": [poly2d_dict],
            "cuboid": [cuboid_dict],
            "poly3d": [poly3d_dict],
            "vec": [seg3d_dict],
        }
    }

@pytest.fixture
def object_data_train_dict(bbox_train_dict) -> dict:
    return {
        "object_data": {
            "bbox": [bbox_train_dict],
        }
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
