# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel


def test_post_init():
    bbox = raillabel.format.Bbox(
        uid="d2764400-8560-4991-a491-ada598b345c8",
        name="test_name",
        pos=raillabel.format.Point2d(0, 1),
        size=raillabel.format.Size2d(2, 3),
    )

    with pytest.raises(TypeError):
        bbox = raillabel.format.Bbox(
            uid="d2764400-8560-4991-a491-ada598b345c8",
            name="test_name",
            pos=raillabel.format.Point2d(0, 1),
        )


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
