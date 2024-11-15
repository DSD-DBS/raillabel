# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from uuid import UUID

from raillabel.format import Metadata, Object, Scene


@dataclass
class SceneBuilder:
    """Use this class for easily creating scenes for tests."""

    result: Scene

    @classmethod
    def empty(cls) -> SceneBuilder:
        """Construct the SceneBuilder with an empty scene."""
        return SceneBuilder(Scene(metadata=Metadata(schema_version="1.0.0")))

    def add_object(
        self,
        object_id: str | UUID | None = None,
        object_type: str | None = None,
        object_name: str | None = None,
    ) -> SceneBuilder:
        """Add an object to a scene."""
        scene = deepcopy(self.result)

        object_type, object_name = _resolve_empty_object_name_or_type(object_type, object_name)
        object_id = _resolve_empty_object_uid(scene, object_id)

        scene.objects[object_id] = Object(object_name, object_type)
        return SceneBuilder(scene)


def _resolve_empty_object_name_or_type(
    object_type: str | None, object_name: str | None
) -> tuple[str, str]:
    if object_name is None and object_type is None:
        object_type = "person"
        object_name = object_type + "_0000"
        return object_type, object_name

    if object_name is None and object_type is not None:
        object_name = object_type + "_0000"
        return object_type, object_name

    if object_name is not None and object_type is None:
        object_type = object_name.split("_")[0]
        return object_type, object_name

    if object_name is not None and object_type is not None:
        return object_type, object_name

    raise RuntimeError


def _resolve_empty_object_uid(scene: Scene, object_id: str | UUID | None) -> UUID:
    if object_id is None:
        uid_index = 0
        while _generate_deterministic_uuid(uid_index, "5c59aad4") in scene.objects:
            uid_index += 1
        object_id = _generate_deterministic_uuid(uid_index, "5c59aad4")

    return UUID(str(object_id))


def _generate_deterministic_uuid(index: int, prefix: str) -> UUID:
    return UUID(f"{prefix.zfill(0)}-0000-4000-0000-{str(index).zfill(12)}")
