# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from raillabel.format.metadata import Metadata


def test_fromdict_minimal():
    metadata = Metadata.fromdict(
        {
            "schema_version": "1.0.0"
        },
        "2.1.1"
    )

    assert metadata.schema_version == "1.0.0"
    assert metadata.subschema_version == "2.1.1"
    assert metadata.annotator is None


def test_fromdict_full():
    metadata = Metadata.fromdict(
        {
            "annotator": "test_annotator",
            "schema_version": "1.0.0",
            "comment": "test_comment",
            "name": "test_project",
            "tagged_file": "test_folder",
        },
        "2.1.1"
    )

    assert metadata.annotator == "test_annotator"
    assert metadata.schema_version == "1.0.0"
    assert metadata.comment == "test_comment"
    assert metadata.name == "test_project"
    assert metadata.subschema_version == "2.1.1"
    assert metadata.tagged_file == "test_folder"


def test_asdict_minimal():
    metadata_dict = Metadata(
        schema_version="1.0.0"
    ).asdict()

    assert metadata_dict == {
        "schema_version": "1.0.0"
    }
def test_asdict_full():
    metadata_dict = Metadata(
        annotator="test_annotator",
        schema_version="1.0.0",
        comment="test_comment",
        name="test_project",
        subschema_version="2.1.1",
        tagged_file="test_folder",
    ).asdict()

    assert metadata_dict == {
        "annotator": "test_annotator",
        "schema_version": "1.0.0",
        "comment": "test_comment",
        "name": "test_project",
        "subschema_version": "2.1.1",
        "tagged_file": "test_folder",
    }

# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])