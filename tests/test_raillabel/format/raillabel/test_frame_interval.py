# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import FrameInterval

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


def test_from_frame_uids_empty():
    frame_uids = []

    assert FrameInterval.from_frame_uids(frame_uids) == []

def test_from_frame_uids_one_frame():
    frame_uids = [1]

    assert FrameInterval.from_frame_uids(frame_uids) == [
        FrameInterval(1, 1)
    ]

def test_from_frame_uids_one_interval():
    frame_uids = [1, 2, 3, 4]

    assert FrameInterval.from_frame_uids(frame_uids) == [
        FrameInterval(1, 4)
    ]

def test_from_frame_uids_multiple_intervals():
    frame_uids = [0, 1, 2, 3, 6, 7, 9, 12, 13, 14]

    assert FrameInterval.from_frame_uids(frame_uids) == [
        FrameInterval(0, 3),
        FrameInterval(6, 7),
        FrameInterval(9, 9),
        FrameInterval(12, 14),
    ]

def test_from_frame_uids_unsorted():
    frame_uids = [5, 2, 1, 3]

    assert FrameInterval.from_frame_uids(frame_uids) == [
        FrameInterval(1, 3),
        FrameInterval(5, 5),
    ]


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
