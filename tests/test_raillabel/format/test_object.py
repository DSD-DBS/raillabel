# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel.format.object import Object

# == Fixtures =========================

@pytest.fixture
def object_person_dict() -> dict:
    return {
        "object_uid": "b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        "data_dict": {
            "name": "person_0000",
            "type": "person",
        },
    }

@pytest.fixture
def object_person() -> dict:
    return Object(
        uid="b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        name="person_0000",
        type="person",
    )

# == Tests ============================

def test_fromdict():
    object = Object.fromdict(
        object_uid="b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        data_dict={
            "name": "person_0000",
            "type": "person",
        }
    )

    assert object.uid == "b40ba3ad-0327-46ff-9c28-2506cfd6d934"
    assert object.name == "person_0000"
    assert object.type == "person"


def test_asdict():
    object = Object(
        uid="b40ba3ad-0327-46ff-9c28-2506cfd6d934",
        name="person_0000",
        type="person",
    )

    assert object.asdict() == {
        "name": "person_0000",
        "type": "person",
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
