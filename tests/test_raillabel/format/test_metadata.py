# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel.format.metadata import Metadata

# == Fixtures =========================

@pytest.fixture
def metadata_minimal() -> dict:
    return {
        "schema_version": "1.0.0"
    }


@pytest.fixture
def metadata_full() -> dict:
    return {
        "schema_version": "1.0.0",
        "annotator": "test_annotator",
        "schema_version": "1.0.0",
        "comment": "test_comment",
        "name": "test_project",
        "tagged_file": "test_folder",
    }

# == Tests ============================

def test_fromdict_minimal(metadata_minimal):
    metadata = Metadata.fromdict(
        metadata_minimal,
        "2.1.1"
    )

    assert metadata.schema_version == "1.0.0"
    assert metadata.subschema_version == "2.1.1"
    assert metadata.annotator is None


def test_fromdict_full(metadata_full):
    metadata = Metadata.fromdict(
        metadata_full,
        "2.1.1"
    )

    assert metadata.annotator == "test_annotator"
    assert metadata.schema_version == "1.0.0"
    assert metadata.comment == "test_comment"
    assert metadata.name == "test_project"
    assert metadata.subschema_version == "2.1.1"
    assert metadata.tagged_file == "test_folder"


def test_fromdict_additional_arg_valid():
    metadata = Metadata.fromdict(
        {
            "schema_version": "1.0.0",
            "additional_argument": "Some Value"
        }
    )

    assert metadata.schema_version == "1.0.0"
    assert metadata.additional_argument == "Some Value"


def test_fromdict_additional_arg_invalid():
    with pytest.raises(KeyError):
        Metadata.fromdict(
            {
                "schema_version": "1.0.0",
                "invalid python variable": "Some Value"
            }
        )


def test_asdict_minimal(metadata_minimal):
    metadata_dict = Metadata(
        schema_version="1.0.0"
    ).asdict()

    assert metadata_dict == metadata_minimal


def test_asdict_full(metadata_full):
    metadata_dict = Metadata(
        annotator="test_annotator",
        schema_version="1.0.0",
        comment="test_comment",
        name="test_project",
        subschema_version="2.1.1",
        tagged_file="test_folder",
    ).asdict()

    assert metadata_dict == metadata_full


def test_fromdict_additional_arg():
    metadata = Metadata(
        schema_version="1.0.0"
    )

    metadata.additional_argument = "Some Value"

    assert metadata.asdict() == {
        "schema_version": "1.0.0",
        "additional_argument": "Some Value"
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
