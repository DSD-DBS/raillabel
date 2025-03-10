# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from raillabel.format import (
    Bbox,
    Camera,
    Cuboid,
    Frame,
    GpsImu,
    IntrinsicsPinhole,
    IntrinsicsRadar,
    Lidar,
    Metadata,
    Object,
    OtherSensor,
    Point2d,
    Point3d,
    Poly2d,
    Poly3d,
    Quaternion,
    Radar,
    Scene,
    Seg3d,
    SensorReference,
    Size2d,
    Size3d,
)
from raillabel.format._util import _flatten_list


@dataclass
class SceneBuilder:
    """Use this class for easily creating scenes for tests."""

    _result: Scene

    @property
    def result(self) -> Scene:
        """Return the scene built by this SceneBuilder."""
        return _add_sensor_reference_to_frames(self._result)

    @result.setter
    def result(self, new_result: Scene) -> None:
        self._result = new_result

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
        scene = deepcopy(self._result)

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
        scene = deepcopy(self._result)

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

    def add_frame(self, frame_id: int | None = None, timestamp: float | None = None) -> SceneBuilder:
        """Add a frame to the scene.

        If no frame_id is provided, the frame_id is the lowest number not currently occupied by
        another frame_id.

        Example:

        .. code-block:: python

            scene = (
                SceneBuilder.empty()
                    .add_frame(frame_id=1)
                    .add_frame(frame_id=3)
                    .add_frame()
                    ._result
            )
            assert sorted(list(scene.frames.keys())) == [1, 2, 3]
        """
        scene = deepcopy(self._result)

        if frame_id is None:
            frame_id = 1
            while frame_id in scene.frames:
                frame_id += 1

        scene.frames[frame_id] = Frame(
            timestamp=Decimal(timestamp) if timestamp is not None else None
        )

        return SceneBuilder(scene)

    def add_annotation(
        self,
        annotation: Bbox | Cuboid | Poly2d | Poly3d | Seg3d,
        uid: str | UUID | None = None,
        frame_id: int = 1,
        object_name: str = "person_0001",
        sensor_id: str = "rgb_center",
    ) -> SceneBuilder:
        """Add an annotation to the scene."""
        new_builder = deepcopy(self)

        uid = _resolve_empty_annotation_uid(new_builder.result, uid)

        if not _is_object_name_object(object_name, new_builder.result):
            new_builder = new_builder.add_object(object_name=object_name)

        if sensor_id not in new_builder.result.sensors:
            new_builder = new_builder.add_sensor(sensor_id)

        if frame_id not in new_builder.result.frames:
            new_builder = new_builder.add_frame(frame_id=frame_id)

        annotation.object_id = _get_object_uid_from_name(object_name, new_builder.result)
        annotation.sensor_id = sensor_id

        new_builder.result.frames[frame_id].annotations[uid] = annotation
        return new_builder

    def add_bbox(
        self,
        uid: str | UUID | None = None,
        pos: Point2d | None = None,
        size: Size2d | None = None,
        frame_id: int = 1,
        object_name: str = "person_0001",
        sensor_id: str = "rgb_center",
        attributes: dict | None = None,
    ) -> SceneBuilder:
        """Add a bbox to the scene."""
        bbox = Bbox(
            object_id=UUID("ffffffff-ffff-4fff-ffff-ffffffffffff"),
            sensor_id=sensor_id,
            pos=pos if pos is not None else Point2d(0, 0),
            size=size if size is not None else Size2d(0, 0),
            attributes=attributes if attributes is not None else {},
        )
        return self.add_annotation(
            annotation=bbox,
            uid=uid,
            frame_id=frame_id,
            object_name=object_name,
            sensor_id=sensor_id,
        )

    def add_cuboid(
        self,
        uid: str | UUID | None = None,
        pos: Point3d | None = None,
        quat: Quaternion | None = None,
        size: Size3d | None = None,
        frame_id: int = 1,
        object_name: str = "person_0001",
        sensor_id: str = "lidar",
        attributes: dict | None = None,
    ) -> SceneBuilder:
        """Add a cuboid to the scene."""
        cuboid = Cuboid(
            object_id=UUID("ffffffff-ffff-4fff-ffff-ffffffffffff"),
            sensor_id=sensor_id,
            pos=pos if pos is not None else Point3d(0, 0, 0),
            size=size if size is not None else Size3d(0, 0, 0),
            quat=quat if quat is not None else Quaternion(0, 0, 0, 0),
            attributes=attributes if attributes is not None else {},
        )
        return self.add_annotation(
            annotation=cuboid,
            uid=uid,
            frame_id=frame_id,
            object_name=object_name,
            sensor_id=sensor_id,
        )

    def add_poly2d(
        self,
        uid: str | UUID | None = None,
        points: list[Point2d] | None = None,
        frame_id: int = 1,
        object_name: str = "person_0001",
        sensor_id: str = "rgb_center",
        attributes: dict | None = None,
    ) -> SceneBuilder:
        """Add a poly2d to the scene."""
        poly2d = Poly2d(
            object_id=UUID("ffffffff-ffff-4fff-ffff-ffffffffffff"),
            sensor_id=sensor_id,
            points=points if points is not None else [],
            closed=False,
            attributes=attributes if attributes is not None else {},
        )
        return self.add_annotation(
            annotation=poly2d,
            uid=uid,
            frame_id=frame_id,
            object_name=object_name,
            sensor_id=sensor_id,
        )

    def add_poly3d(
        self,
        uid: str | UUID | None = None,
        points: list[Point3d] | None = None,
        frame_id: int = 1,
        object_name: str = "person_0001",
        sensor_id: str = "lidar",
        attributes: dict | None = None,
    ) -> SceneBuilder:
        """Add a poly3d to the scene."""
        poly3d = Poly3d(
            object_id=UUID("ffffffff-ffff-4fff-ffff-ffffffffffff"),
            sensor_id=sensor_id,
            points=points if points is not None else [],
            closed=False,
            attributes=attributes if attributes is not None else {},
        )
        return self.add_annotation(
            annotation=poly3d,
            uid=uid,
            frame_id=frame_id,
            object_name=object_name,
            sensor_id=sensor_id,
        )

    def add_seg3d(
        self,
        uid: str | UUID | None = None,
        point_ids: list[int] | None = None,
        frame_id: int = 1,
        object_name: str = "person_0001",
        sensor_id: str = "lidar",
        attributes: dict | None = None,
    ) -> SceneBuilder:
        """Add a poly3d to the scene."""
        seg3d = Seg3d(
            object_id=UUID("ffffffff-ffff-4fff-ffff-ffffffffffff"),
            sensor_id=sensor_id,
            point_ids=point_ids if point_ids is not None else [],
            attributes=attributes if attributes is not None else {},
        )
        return self.add_annotation(
            annotation=seg3d,
            uid=uid,
            frame_id=frame_id,
            object_name=object_name,
            sensor_id=sensor_id,
        )


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


def _resolve_empty_annotation_uid(scene: Scene, uid: str | UUID | None) -> UUID:
    if uid is None:
        annotation_uids_in_scene = set(
            _flatten_list([tuple(frame.annotations.keys()) for frame in scene.frames.values()])
        )
        uid_index = 0
        while _generate_deterministic_uuid(uid_index, "6c95543d") in annotation_uids_in_scene:
            uid_index += 1

        uid = _generate_deterministic_uuid(uid_index, "6c95543d")

    return UUID(str(uid))


def _is_object_name_object(object_name: str, scene: Scene) -> bool:
    return any(object_.name == object_name for object_ in scene.objects.values())


def _get_object_uid_from_name(object_name: str, scene: Scene) -> UUID:
    for object_uid, object_ in scene.objects.items():
        if object_.name == object_name:
            return object_uid

    raise RuntimeError


def _add_sensor_reference_to_frames(scene: Scene) -> Scene:
    for frame in scene.frames.values():
        if frame.timestamp is None:
            continue
        frame.sensors = {sensor_id: SensorReference(frame.timestamp) for sensor_id in scene.sensors}
    return scene
