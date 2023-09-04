# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import _ObjectAnnotation

# == Fixtures =========================

@pytest.fixture
def attributes_single_type_dict() -> dict:
    return {
        "text": [
            {
                "name": "test_text_attr0",
                "val": "test_text_attr0_val"
            },
            {
                "name": "test_text_attr1",
                "val": "test_text_attr1_val"
            }
        ]
    }

@pytest.fixture
def attributes_single_type() -> dict:
    return {
        "test_text_attr0": "test_text_attr0_val",
        "test_text_attr1": "test_text_attr1_val",
    }


@pytest.fixture
def attributes_multiple_types_dict() -> dict:
    return {
        "text": [{
            "name": "text_attr",
            "val": "text_val"
        }],
        "num": [{
            "name": "num_attr",
            "val": 0
        }],
        "boolean": [{
            "name": "bool_attr",
            "val": True
        }],
        "vec": [{
            "name": "vec_attr",
            "val": [0, 1, 2]
        }],
    }

@pytest.fixture
def attributes_multiple_types() -> dict:
    return {
        "text_attr": "text_val",
        "num_attr": 0,
        "bool_attr": True,
        "vec_attr": [0, 1, 2],
    }

# == Tests ============================

def test_fromdict__single_type():
    attributes_dict = {
        "attributes": {
            "text": [
                {
                    "name": "test_text_attr0",
                    "val": "test_text_attr0_val"
                },
                {
                    "name": "test_text_attr1",
                    "val": "test_text_attr1_val"
                }
            ]
        }
    }

    assert _ObjectAnnotation._attributes_fromdict(attributes_dict) == {
        "test_text_attr0": "test_text_attr0_val",
        "test_text_attr1": "test_text_attr1_val",
    }

def test_fromdict__multiple_types():
    attributes_dict = {
        "attributes": {
            "text": [{
                "name": "text_attr",
                "val": "text_val"
            }],
            "num": [{
                "name": "num_attr",
                "val": 0
            }],
            "boolean": [{
                "name": "bool_attr",
                "val": True
            }],
            "vec": [{
                "name": "vec_attr",
                "val": [0, 1, 2]
            }],
        }
    }

    assert _ObjectAnnotation._attributes_fromdict(attributes_dict) == {
        "text_attr": "text_val",
        "num_attr": 0,
        "bool_attr": True,
        "vec_attr": [0, 1, 2],
    }


def test_asdict__single_type():
    attributes = {
        "test_text_attr0": "test_text_attr0_val",
        "test_text_attr1": "test_text_attr1_val",
    }

    assert _ObjectAnnotation._attributes_asdict(None, attributes) == {
        "text": [
            {
                "name": "test_text_attr0",
                "val": "test_text_attr0_val"
            },
            {
                "name": "test_text_attr1",
                "val": "test_text_attr1_val"
            }
        ]
    }

def test_asdict__multiple_types():
    attributes = {
        "text_attr": "text_val",
        "num_attr": 0,
        "bool_attr": True,
        "vec_attr": [0, 1, 2],
    }

    assert _ObjectAnnotation._attributes_asdict(None, attributes) == {
        "text": [{
            "name": "text_attr",
            "val": "text_val"
        }],
        "num": [{
            "name": "num_attr",
            "val": 0
        }],
        "boolean": [{
            "name": "bool_attr",
            "val": True
        }],
        "vec": [{
            "name": "vec_attr",
            "val": [0, 1, 2]
        }],
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
