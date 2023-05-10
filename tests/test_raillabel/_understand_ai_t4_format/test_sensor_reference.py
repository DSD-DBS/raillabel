# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel._understand_ai_t4_format as uai_format


def test_fromdict():
    sensor_reference = uai_format.SensorReference.fromdict({
        "type": "test_id",
        "uri": "test_folder/000_1632321843.100464380.png",
        "timestamp": "1632321843.100464380"
    })

    assert sensor_reference.type == "test_id"
    assert sensor_reference.uri == "test_folder/000_1632321843.100464380.png"
    assert sensor_reference.timestamp == Decimal("1632321843.100464380")

# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
