# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel.format import Frame, FrameInterval, Scene

# == Fixtures =========================

@pytest.fixture
def scene_minimal_dict(metadata_minimal_dict) -> Scene:
    return {
        "openlabel": {
            "metadata": metadata_minimal_dict
        }
    }

@pytest.fixture
def scene_minimal(metadata_minimal) -> Scene:
    return Scene(
        metadata=metadata_minimal
    )

# == Tests ============================

def test_frame_intervals(metadata_minimal):
    scene = Scene(
        metadata=metadata_minimal,
        frames={
            1: Frame(1),
            2: Frame(2),
            3: Frame(3),
            8: Frame(8),
        }
    )

    assert scene.frame_intervals == [
        FrameInterval(1, 3),
        FrameInterval(8, 8),
    ]


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
