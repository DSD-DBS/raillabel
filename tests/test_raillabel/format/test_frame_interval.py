# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel.format.frame_interval import FrameInterval

# == Fixtures =========================

@pytest.fixture
def frame_interval_dict() -> dict:
    return {
        "frame_start": 12,
        "frame_end": 16
    }

@pytest.fixture
def frame_interval() -> dict:
    return FrameInterval(
        frame_start=12,
        frame_end=16,
    )

# == Tests ============================

def test_fromdict():
    frame_interval = FrameInterval.fromdict(
        {
            "frame_start": 12,
            "frame_end": 16,
        }
    )

    assert frame_interval.frame_start == 12
    assert frame_interval.frame_end == 16


def test_asdict():
    frame_interval = FrameInterval(
        frame_start=12,
        frame_end=16,
    )

    assert frame_interval.asdict() == {
        "frame_start": 12,
        "frame_end": 16,
    }


def test_len():
    frame_interval = FrameInterval(
        frame_start=12,
        frame_end=16,
    )

    assert len(frame_interval) == 5


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
