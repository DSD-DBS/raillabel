# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from uuid import UUID

from raillabel.filter._filter_abc import _AnnotationLevelFilter, _FilterAbc, _FrameLevelFilter
from raillabel.json_format import (
    JSONCoordinateSystem,
    JSONFrame,
    JSONObject,
    JSONScene,
    JSONSceneContent,
    JSONStreamCamera,
    JSONStreamOther,
    JSONStreamRadar,
)

from .bbox import Bbox
from .camera import Camera
from .cuboid import Cuboid
from .frame import Frame
from .frame_interval import FrameInterval
from .gps_imu import GpsImu
from .lidar import Lidar
from .metadata import Metadata
from .object import Object
from .other_sensor import OtherSensor
from .poly2d import Poly2d
from .poly3d import Poly3d
from .radar import Radar
from .seg3d import Seg3d


@dataclass
class Scene:
    """The root RailLabel class, which contains all data.

    Examples:
    You can load scenes like this:

    .. code-block:: python

        import raillabel
        scene = raillabel.load("path/to/scene.json")

    The scenes then contain all of the data. This is how you can iterate over the annotations:

    .. code-block:: python

        for frame in scene.frames.values():
            for annotation in frame.annotations.values():
                pass  # do something with the annotation here
    """

    metadata: Metadata
    "Container of information about the annotation file itself."

    sensors: dict[str, Camera | Lidar | Radar | GpsImu | OtherSensor] = field(default_factory=dict)
    "The sensors used in this scene. Keys are sensor names."

    objects: dict[UUID, Object] = field(default_factory=dict)
    "Unique objects (like a specific person) in this scene. Keys are object uuids"

    frames: dict[int, Frame] = field(default_factory=dict)
    "A container of dynamic, timewise, information. Keys are the frame integer number."

    @classmethod
    def from_json(cls, json: JSONScene) -> Scene:
        """Construct a scene from a json object."""
        return Scene(
            metadata=Metadata.from_json(json.openlabel.metadata),
            sensors=_sensors_from_json(json.openlabel.streams, json.openlabel.coordinate_systems),
            objects=_objects_from_json(json.openlabel.objects),
            frames=_frames_from_json(json.openlabel.frames),
        )

    def to_json(self) -> JSONScene:
        """Export this scene into the RailLabel JSON format."""
        return JSONScene(
            openlabel=JSONSceneContent(
                metadata=self.metadata.to_json(),
                streams={
                    sensor_id: sensor.to_json()[0] for sensor_id, sensor in self.sensors.items()
                },
                coordinate_systems=_coordinate_systems_to_json(self.sensors),
                objects={
                    obj_id: obj.to_json(obj_id, self.frames) for obj_id, obj in self.objects.items()
                },
                frames={
                    frame_id: frame.to_json(self.objects) for frame_id, frame in self.frames.items()
                },
                frame_intervals=[
                    fi.to_json() for fi in FrameInterval.from_frame_ids(list(self.frames.keys()))
                ],
            )
        )

    def filter(self, filters: list[_FilterAbc]) -> Scene:
        """Return a scene with annotations, sensors, objects and frames excluded.

        Example:

        .. code-block:: python

            from raillabel.filter import (
                IncludeObjectTypeFilter,
                ExcludeAnnotationTypeFilter,
                StartTimeFilter, ExcludeFrameIdFilter,
                IncludeAttributesFilter
            )

            scene_with_only_trains = scene.filter([IncludeObjectTypeFilter(["rail_vehicle"])])

            scene_without_bboxs = scene.filter([ExcludeAnnotationTypeFilter(["bbox"])])

            cut_scene_with_only_red_trains = scene.filter([
                StartTimeFilter("1587349200.004200000"),
                ExcludeFrameIdFilter([2, 4]),
                IncludeObjectTypeFilter(["rail_vehicle"]),
                IncludeAttributesFilter({"color": "red"}),
            ])
        """
        frame_filters, annotation_filters = _separate_filters(filters)

        filtered_scene = Scene(metadata=deepcopy(self.metadata))
        filtered_scene.frames = _filter_frames(self, frame_filters, annotation_filters)
        filtered_scene.sensors = _get_used_sensors(self, filtered_scene)
        filtered_scene.objects = _get_used_objects(self, filtered_scene)

        return _remove_unused_sensor_references(filtered_scene)


def _sensors_from_json(
    json_streams: dict[str, JSONStreamCamera | JSONStreamOther | JSONStreamRadar] | None,
    json_coordinate_systems: dict[str, JSONCoordinateSystem] | None,
) -> dict[str, Camera | Lidar | Radar | GpsImu | OtherSensor]:
    sensors: dict[str, Camera | Lidar | Radar | GpsImu | OtherSensor] = {}

    if json_streams is None or json_coordinate_systems is None:
        return sensors

    for sensor_id, json_stream in json_streams.items():
        json_coordinate_system = json_coordinate_systems[sensor_id]

        if isinstance(json_stream, JSONStreamCamera):
            sensors[sensor_id] = Camera.from_json(json_stream, json_coordinate_system)

        if isinstance(json_stream, JSONStreamRadar):
            sensors[sensor_id] = Radar.from_json(json_stream, json_coordinate_system)

        if isinstance(json_stream, JSONStreamOther) and json_stream.type == "lidar":
            sensors[sensor_id] = Lidar.from_json(json_stream, json_coordinate_system)

        if isinstance(json_stream, JSONStreamOther) and json_stream.type == "gps_imu":
            sensors[sensor_id] = GpsImu.from_json(json_stream, json_coordinate_system)

        if isinstance(json_stream, JSONStreamOther) and json_stream.type == "other":
            sensors[sensor_id] = OtherSensor.from_json(json_stream, json_coordinate_system)

    return sensors


def _objects_from_json(json_objects: dict[UUID, JSONObject] | None) -> dict[UUID, Object]:
    if json_objects is None:
        return {}

    return {obj_id: Object.from_json(json_obj) for obj_id, json_obj in json_objects.items()}


def _frames_from_json(json_frames: dict[int, JSONFrame] | None) -> dict[int, Frame]:
    if json_frames is None:
        return {}

    return {frame_id: Frame.from_json(json_frame) for frame_id, json_frame in json_frames.items()}


def _coordinate_systems_to_json(
    sensors: dict[str, Camera | Lidar | Radar | GpsImu | OtherSensor],
) -> dict[str, JSONCoordinateSystem]:
    json_coordinate_systems = {
        sensor_id: sensor.to_json()[1] for sensor_id, sensor in sensors.items()
    }
    json_coordinate_systems["base"] = JSONCoordinateSystem(
        parent="",
        type="local",
        pose_wrt_parent=None,
        children=list(json_coordinate_systems.keys()),
    )
    return json_coordinate_systems


def _separate_filters(
    all_filters: list[_FilterAbc],
) -> tuple[list[_FrameLevelFilter], list[_AnnotationLevelFilter]]:
    frame_filters = []
    annotation_filters = []
    for filter_ in all_filters:
        if isinstance(filter_, _FrameLevelFilter):
            frame_filters.append(filter_)

        if isinstance(filter_, _AnnotationLevelFilter):
            annotation_filters.append(filter_)

    return frame_filters, annotation_filters


def _filter_frames(
    scene: Scene,
    frame_filters: list[_FrameLevelFilter],
    annotation_filters: list[_AnnotationLevelFilter],
) -> dict[int, Frame]:
    filtered_frames = {}

    for frame_id, frame in scene.frames.items():
        if _frame_passes_all_filters(frame_id, frame, frame_filters):
            filtered_frames[frame_id] = Frame(
                timestamp=deepcopy(frame.timestamp),
                sensors=deepcopy(frame.sensors),
                frame_data=deepcopy(frame.frame_data),
                annotations=_filter_annotations(frame, annotation_filters, scene),
            )

    return filtered_frames


def _filter_annotations(
    frame: Frame, annotation_filters: list[_AnnotationLevelFilter], scene: Scene
) -> dict[UUID, Bbox | Cuboid | Poly2d | Poly3d | Seg3d]:
    annotations = {}

    for annotation_id, annotation in frame.annotations.items():
        if _annotation_passes_all_filters(annotation_id, annotation, annotation_filters, scene):
            annotations[annotation_id] = deepcopy(annotation)

    return annotations


def _frame_passes_all_filters(
    frame_id: int, frame: Frame, frame_filters: list[_FrameLevelFilter]
) -> bool:
    return all(filter_.passes_filter(frame_id, frame) for filter_ in frame_filters)


def _annotation_passes_all_filters(
    annotation_id: UUID,
    annotation: Bbox | Cuboid | Poly2d | Poly3d | Seg3d,
    annotation_filters: list[_AnnotationLevelFilter],
    scene: Scene,
) -> bool:
    return all(
        filter_.passes_filter(annotation_id, annotation, scene) for filter_ in annotation_filters
    )


def _get_used_sensors(
    scene: Scene, filtered_scene: Scene
) -> dict[str, Camera | Lidar | Radar | GpsImu | OtherSensor]:
    used_sensors = {}
    for frame in filtered_scene.frames.values():
        for annotation in frame.annotations.values():
            if annotation.sensor_id not in used_sensors:
                used_sensors[annotation.sensor_id] = deepcopy(scene.sensors[annotation.sensor_id])

    return used_sensors


def _get_used_objects(scene: Scene, filtered_scene: Scene) -> dict[UUID, Object]:
    used_objects = {}
    for frame in filtered_scene.frames.values():
        for annotation in frame.annotations.values():
            if annotation.object_id not in used_objects:
                used_objects[annotation.object_id] = deepcopy(scene.objects[annotation.object_id])

    return used_objects


def _remove_unused_sensor_references(filtered_scene: Scene) -> Scene:
    for frame in filtered_scene.frames.values():
        unused_sensor_reference_ids = [
            sensor_id for sensor_id in frame.sensors if sensor_id not in filtered_scene.sensors
        ]
        for unused_sensor_id in unused_sensor_reference_ids:
            del frame.sensors[unused_sensor_id]
    return filtered_scene
