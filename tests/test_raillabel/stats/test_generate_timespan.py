# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel

# == Fixtures ============================

@pytest.fixture
def metadata() -> raillabel.format.Metadata:
    return raillabel.format.Metadata(schema_version="1.0.0")

# == Tests ============================

def test_simple_timespan(metadata):
    scene = raillabel.Scene(
        metadata=metadata,
        frames={
            0: raillabel.format.Frame(
                uid=0,
                timestamp=100
            ),
            1: raillabel.format.Frame(
                uid=1,
                timestamp=105
            ),
            2: raillabel.format.Frame(
                uid=0,
                timestamp=110
            ),
        }
    )

    assert raillabel.stats.generate_timespan(scene) == (100, 110)

def test_unordered_timspan(metadata):
    scene = raillabel.Scene(
        metadata=metadata,
        frames={
            0: raillabel.format.Frame(
                uid=0,
                timestamp=110
            ),
            1: raillabel.format.Frame(
                uid=1,
                timestamp=100
            ),
        }
    )

    assert raillabel.stats.generate_timespan(scene) == (100, 110)

def test_empty_timespan(metadata):
    scene = raillabel.Scene(
        metadata=metadata,
        frames={}
    )

    assert raillabel.stats.generate_timespan(scene) == (None, None)


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
