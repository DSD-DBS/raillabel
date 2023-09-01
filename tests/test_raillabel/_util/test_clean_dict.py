# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel._util._clean_dict import _clean_dict


def test_clean_dict():
    input_dict = {
        "non_empty_field": "non_empty_value",
        "none_field": None,
        "field_with_len_0": []
    }

    assert _clean_dict(input_dict) == {
        "non_empty_field": "non_empty_value",
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
