# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from raillabel.json_format import (
    JSONCoordinateSystem,
    JSONScene,
    JSONStreamCamera,
    JSONStreamOther,
    JSONStreamRadar,
)

from .camera import Camera
from .frame import Frame
from .gps_imu import GpsImu
from .lidar import Lidar
from .metadata import Metadata
from .object import Object
from .other_sensor import OtherSensor
from .radar import Radar


@dataclass
class Scene:
    """The root RailLabel class, which contains all data."""

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
        )


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
