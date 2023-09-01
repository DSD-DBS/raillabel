# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel._util._warning import _warning, _WarningsLogger


def test_issue_warning():
    with _WarningsLogger() as logger:
        _warning("lorem ipsum")

    assert logger.warnings == [
        "lorem ipsum"
    ]

def test_handover_exception():
    with pytest.raises(RuntimeError) as error:
        with _WarningsLogger() as logger:
            raise RuntimeError("weewoo something went wrong")

def test_clear_warnings():
    with _WarningsLogger() as logger1:
        _warning("lorem ipsum")

    with _WarningsLogger() as logger2:
        pass

    assert len(logger2.warnings) == 0


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
