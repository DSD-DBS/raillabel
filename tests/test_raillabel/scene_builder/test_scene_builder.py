# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from uuid import UUID

import pytest

import raillabel
from raillabel.format import Scene, Metadata, Object
from raillabel.scene_builder.scene_builder import SceneBuilder


def test_empty():
    actual = SceneBuilder.empty()
    assert actual.result == Scene(Metadata(schema_version="1.0.0"))


def test_add_object__all_options():
    actual = SceneBuilder.empty().add_object(
        object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
        object_type="train",
        object_name="train_0001",
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="train_0001", type="train")
        },
    )


def test_add_object__no_object_name():
    actual = SceneBuilder.empty().add_object(
        object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
        object_type="train",
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="train_0000", type="train")
        },
    )


def test_add_object__no_object_type():
    actual = SceneBuilder.empty().add_object(
        object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
        object_name="train_0000",
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="train_0000", type="train")
        },
    )


def test_add_object__no_object_type_or_name():
    actual = SceneBuilder.empty().add_object(
        object_id="5c59aad4-9fcd-4903-a9fa-72b1b76c23a5",
    )
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-9fcd-4903-a9fa-72b1b76c23a5"): Object(name="person_0000", type="person")
        },
    )


def test_add_object__no_object_id():
    actual = SceneBuilder.empty().add_object(object_type="train", object_name="train_0001")
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="train_0001", type="train")
        },
    )


def test_add_object__object_id_iteration():
    actual = SceneBuilder.empty().add_object().add_object().add_object().add_object()
    assert actual.result == Scene(
        metadata=Metadata(schema_version="1.0.0"),
        objects={
            UUID("5c59aad4-0000-4000-0000-000000000000"): Object(name="person_0000", type="person"),
            UUID("5c59aad4-0000-4000-0000-000000000001"): Object(name="person_0000", type="person"),
            UUID("5c59aad4-0000-4000-0000-000000000002"): Object(name="person_0000", type="person"),
            UUID("5c59aad4-0000-4000-0000-000000000003"): Object(name="person_0000", type="person"),
        },
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
