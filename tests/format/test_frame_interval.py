# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import FrameInterval
from raillabel.json_format import JSONFrameInterval

# == Fixtures =========================


@pytest.fixture
def frame_interval_json() -> JSONFrameInterval:
    return JSONFrameInterval(frame_start=12, frame_end=16)


@pytest.fixture
def frame_interval() -> dict:
    return FrameInterval(
        start=12,
        end=16,
    )


# == Tests ============================


def test_from_json(frame_interval, frame_interval_json):
    actual = FrameInterval.from_json(frame_interval_json)
    assert actual == frame_interval


def test_len():
    frame_interval = FrameInterval(
        start=12,
        end=16,
    )

    assert len(frame_interval) == 5


def test_from_frame_ids_empty():
    frame_ids = []

    assert FrameInterval.from_frame_ids(frame_ids) == []


def test_from_frame_ids_one_frame():
    frame_ids = [1]

    assert FrameInterval.from_frame_ids(frame_ids) == [FrameInterval(1, 1)]


def test_from_frame_ids_one_interval():
    frame_ids = [1, 2, 3, 4]

    assert FrameInterval.from_frame_ids(frame_ids) == [FrameInterval(1, 4)]


def test_from_frame_ids_multiple_intervals():
    frame_ids = [0, 1, 2, 3, 6, 7, 9, 12, 13, 14]

    assert FrameInterval.from_frame_ids(frame_ids) == [
        FrameInterval(0, 3),
        FrameInterval(6, 7),
        FrameInterval(9, 9),
        FrameInterval(12, 14),
    ]


def test_from_frame_ids_unsorted():
    frame_ids = [5, 2, 1, 3]

    assert FrameInterval.from_frame_ids(frame_ids) == [
        FrameInterval(1, 3),
        FrameInterval(5, 5),
    ]


def test_to_json(frame_interval, frame_interval_json):
    actual = frame_interval.to_json()
    assert actual == frame_interval_json


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
