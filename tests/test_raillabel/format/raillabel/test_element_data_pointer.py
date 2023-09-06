# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel._util._attribute_type import AttributeType
from raillabel.format import ElementDataPointer

# == Fixtures =========================

@pytest.fixture
def element_data_pointer_minimal_dict() -> dict:
    return {
        "type": "bbox",
        "frame_intervals": [],
        "attribute_pointers": {},
    }

@pytest.fixture
def element_data_pointer_minimal():
    return ElementDataPointer(
        uid="rgb_middle__bbox__person",
        frame_intervals=[],
        attribute_pointers={}
    )


@pytest.fixture
def element_data_pointer_full_dict(frame_interval_dict) -> dict:
    return {
        "type": "bbox",
        "frame_intervals": [
            frame_interval_dict
        ],
        "attribute_pointers": {
            "text_attr": "text",
            "num_attr": "num",
            "bool_attr": "boolean",
            "vec_attr": "vec",
        },
    }

@pytest.fixture
def element_data_pointer_full(sensor_camera, object_person, frame_interval):
    return ElementDataPointer(
        uid="rgb_middle__bbox__person",
        frame_intervals=[
            frame_interval
        ],
        attribute_pointers={
            "text_attr": AttributeType.TEXT,
            "num_attr": AttributeType.NUM,
            "bool_attr": AttributeType.BOOLEAN,
            "vec_attr": AttributeType.VEC,
        }
    )

# == Tests ============================


def test_asdict_minimal(sensor_camera, object_person):
    element_data_pointer = ElementDataPointer(
        uid="rgb_middle__bbox__person",
        frame_intervals=[],
        attribute_pointers={}
    )

    assert element_data_pointer.asdict() == {
        "type": "bbox",
        "frame_intervals": [],
        "attribute_pointers": {},
    }

def test_asdict_full(sensor_camera, object_person, frame_interval, frame_interval_dict):
    element_data_pointer = ElementDataPointer(
        uid="rgb_middle__bbox__person",
        frame_intervals=[
            frame_interval
        ],
        attribute_pointers={
            "text_attr": AttributeType.TEXT,
            "num_attr": AttributeType.NUM,
            "bool_attr": AttributeType.BOOLEAN,
            "vec_attr": AttributeType.VEC,
        }
    )

    assert element_data_pointer.asdict() == {
        "type": "bbox",
        "frame_intervals": [
            frame_interval_dict
        ],
        "attribute_pointers": {
            "text_attr": "text",
            "num_attr": "num",
            "bool_attr": "boolean",
            "vec_attr": "vec",
        },
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
