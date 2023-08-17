# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel.format.frame_interval import FrameInterval


def test_asdict_valid():
    frame_interval = FrameInterval(0, 1)

    assert frame_interval.asdict() == {
        "frame_start": 0,
        "frame_end": 1
    }


def test_asdict_invalid():
    frame_interval = FrameInterval(0, "invalid_integer")

    with pytest.raises(ValueError):
        frame_interval.asdict()


def test_len():
    frame_interval = FrameInterval(0, 13)

    assert len(frame_interval) == 14


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
