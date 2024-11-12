# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Metadata
from raillabel.json_format import JSONMetadata

# == Fixtures =========================


@pytest.fixture
def metadata_json() -> JSONMetadata:
    return JSONMetadata(
        schema_version="1.0.0",
        name="some_file",
        subschema_version="4.0.0",
        exporter_version="1.2.3",
        file_version="0.1.5",
        tagged_file="path/to/data",
        annotator="John Doe",
        comment="this is a very nice annotation file",
    )


@pytest.fixture
def metadata() -> dict:
    return Metadata(
        schema_version="1.0.0",
        name="some_file",
        subschema_version="4.0.0",
        exporter_version="1.2.3",
        file_version="0.1.5",
        tagged_file="path/to/data",
        annotator="John Doe",
        comment="this is a very nice annotation file",
    )


# == Tests ============================


def test_from_json(metadata, metadata_json):
    actual = Metadata.from_json(metadata_json)
    assert actual == metadata


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
