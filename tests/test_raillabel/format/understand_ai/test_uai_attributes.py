# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import pytest

# == Fixtures =========================

@pytest.fixture
def attributes_uai_dict() -> dict:
    return {
        "isDummy": False,
        "carries": "nothing",
        "connectedTo": [],
        "pose": "upright"
    }

@pytest.fixture
def attributes_uai() -> dict:
    return {
        "isDummy": False,
        "carries": "nothing",
        "connectedTo": [],
        "pose": "upright"
    }

@pytest.fixture
def attributes_raillabel_dict() -> dict:
    return {
        "text": [
            {
                "name": "carries",
                "val": "nothing"
            },
            {
                "name": "pose",
                "val": "upright"
            }
        ],
        "boolean": [
            {
                "name": "isDummy",
                "val": False
            }
        ],
        "vec": [
            {
                "name": "connectedTo",
                "val": []
            }
        ]
    }
