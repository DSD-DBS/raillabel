# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from uuid import UUID

from raillabel.format import (
    Camera,
    GpsImu,
    IntrinsicsPinhole,
    IntrinsicsRadar,
    Lidar,
    Metadata,
    Object,
    OtherSensor,
    Radar,
    Scene,
)


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
        """Add an object to the scene."""
        scene = deepcopy(self.result)

        object_type, object_name = _resolve_empty_object_name_or_type(object_type, object_name)
        object_id = _resolve_empty_object_uid(scene, object_id)

        scene.objects[object_id] = Object(object_name, object_type)
        return SceneBuilder(scene)

    def add_sensor(self, sensor_id: str) -> SceneBuilder:
        """Add a sensor to the scene.

        The sensor type is implicitly determined by the sensor_id. Id's, that start with 'rgb_' or
        'ir_' are added as a camera. If the id is 'lidar', it is a lidar. 'radar' creates a Radar.
        'gps_imu' creates a GpsImu. If the id does not match any of these, a OtherSensor is added.
        """
        scene = deepcopy(self.result)

        truncated_sensor_id = sensor_id.split("_")[0].lower()

        if truncated_sensor_id in ["rgb", "ir"]:
            scene.sensors[sensor_id] = Camera(
                intrinsics=IntrinsicsPinhole(
                    camera_matrix=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                    distortion=(0, 0, 0, 0, 0),
                    width_px=0,
                    height_px=0,
                )
            )

        elif truncated_sensor_id == "radar":
            scene.sensors[sensor_id] = Radar(
                intrinsics=IntrinsicsRadar(resolution_px_per_m=0, width_px=0, height_px=0)
            )

        elif truncated_sensor_id == "lidar":
            scene.sensors[sensor_id] = Lidar()

        elif truncated_sensor_id == "gps":
            scene.sensors[sensor_id] = GpsImu()

        else:
            scene.sensors[sensor_id] = OtherSensor()

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

    raise RuntimeError  # this part is unreachable but this is the only way that mypy is happy


def _resolve_empty_object_uid(scene: Scene, object_id: str | UUID | None) -> UUID:
    if object_id is None:
        uid_index = 0
        while _generate_deterministic_uuid(uid_index, "5c59aad4") in scene.objects:
            uid_index += 1

        object_id = _generate_deterministic_uuid(uid_index, "5c59aad4")

    return UUID(str(object_id))


def _generate_deterministic_uuid(index: int, prefix: str) -> UUID:
    return UUID(f"{prefix.zfill(0)}-0000-4000-0000-{str(index).zfill(12)}")
