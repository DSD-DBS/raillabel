# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel._understand_ai_t4_format as uai_format


def test_fromdict():
    input_data = {
        "height": 12.887274595406309,
        "width": 0.9726718154765793,
        "length": 0.7487449536720978

    }
    size = uai_format.Size3d.fromdict(input_data)

    assert size.height == float(input_data["height"])
    assert size.width == float(input_data["width"])
    assert size.length == float(input_data["length"])

# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
