# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import typing as t
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

from raillabel.format import Sensor, SensorType

# == Fixtures =========================

@pytest.fixture
def sensors(sensor_lidar, sensor_camera, sensor_radar) -> t.Dict[str, Sensor]:
    return {
        sensor_lidar.uid: sensor_lidar,
        sensor_camera.uid: sensor_camera,
        sensor_radar.uid: sensor_radar,
    }

@pytest.fixture
def streams_dict(sensor_camera_dict, sensor_lidar_dict, sensor_radar_dict) -> dict:
    return {
        sensor_camera_dict["uid"]: sensor_camera_dict["stream"],
        sensor_lidar_dict["uid"]: sensor_lidar_dict["stream"],
        sensor_radar_dict["uid"]: sensor_radar_dict["stream"],
    }

@pytest.fixture
def coordinate_systems_dict(sensor_camera_dict, sensor_lidar_dict, sensor_radar_dict) -> dict:
    return {
        "base": {
            "type": "local",
            "parent": "",
            "children": [
                sensor_lidar_dict["uid"],
                sensor_camera_dict["uid"],
                sensor_radar_dict["uid"],
            ]
        },
        sensor_camera_dict["uid"]: sensor_camera_dict["coordinate_system"],
        sensor_lidar_dict["uid"]: sensor_lidar_dict["coordinate_system"],
        sensor_radar_dict["uid"]: sensor_radar_dict["coordinate_system"],
    }


@pytest.fixture
def sensor_lidar_dict(transform_dict) -> dict:
    return {
        "uid": "lidar",
        "stream": {
            "type": "lidar",
            "uri": "/lidar_merged",
        },
        "coordinate_system": {
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": transform_dict,
        }
    }

@pytest.fixture
def sensor_lidar(transform) -> Sensor:
    return Sensor(
        uid="lidar",
        extrinsics=transform,
        intrinsics=None,
        type=SensorType.LIDAR,
        uri="/lidar_merged",
    )


@pytest.fixture
def sensor_camera_dict(transform_dict, intrinsics_pinhole_dict) -> dict:
    return {
        "uid": "rgb_middle",
        "stream": {
            "type": "camera",
            "uri": "/S1206063/image",
            "stream_properties": {
                "intrinsics_pinhole": intrinsics_pinhole_dict
            }
        },
        "coordinate_system": {
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": transform_dict,
        }
    }

@pytest.fixture
def sensor_camera(transform, intrinsics_pinhole) -> Sensor:
    return Sensor(
        uid="rgb_middle",
        extrinsics=transform,
        intrinsics=intrinsics_pinhole,
        type=SensorType.CAMERA,
        uri="/S1206063/image",
    )


@pytest.fixture
def sensor_radar_dict(transform_dict, intrinsics_radar_dict) -> dict:
    return {
        "uid": "radar",
        "stream": {
            "type": "radar",
            "uri": "/talker1/Nvt/Cartesian",
            "stream_properties": {
                "intrinsics_radar": intrinsics_radar_dict
            }
        },
        "coordinate_system": {
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": transform_dict,
        }
    }

@pytest.fixture
def sensor_radar(transform, intrinsics_radar) -> Sensor:
    return Sensor(
        uid="radar",
        extrinsics=transform,
        intrinsics=intrinsics_radar,
        type=SensorType.RADAR,
        uri="/talker1/Nvt/Cartesian",
    )

# == Tests ============================

def test_lidar_fromdict(transform, transform_dict):
    sensor = Sensor.fromdict(
        uid="lidar",
        stream_data_dict={
            "type": "lidar",
            "uri": "/lidar_merged",
        },
        cs_data_dict={
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": transform_dict,
        }
    )

    assert sensor.uid == "lidar"
    assert sensor.extrinsics == transform
    assert sensor.intrinsics == None
    assert sensor.type == SensorType.LIDAR
    assert sensor.uri == "/lidar_merged"

def test_lidar_asdict(transform, transform_dict):
    sensor = Sensor(
        uid="lidar",
        extrinsics=transform,
        intrinsics=None,
        type=SensorType.LIDAR,
        uri="/lidar_merged",
    )

    assert sensor.asdict() == {
        "stream": {
            "type": "lidar",
            "uri": "/lidar_merged",
        },
        "coordinate_system": {
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": transform_dict,
        }
    }


def test_camera_fromdict(transform, transform_dict, intrinsics_pinhole, intrinsics_pinhole_dict):
    sensor = Sensor.fromdict(
        uid="rgb_middle",
        stream_data_dict={
            "type": "camera",
            "uri": "/S1206063/image",
            "stream_properties": {
                "intrinsics_pinhole": intrinsics_pinhole_dict
            }
        },
        cs_data_dict={
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": transform_dict,
        }
    )

    assert sensor.uid == "rgb_middle"
    assert sensor.extrinsics == transform
    assert sensor.intrinsics == intrinsics_pinhole
    assert sensor.type == SensorType.CAMERA
    assert sensor.uri == "/S1206063/image"

def test_camera_asdict(transform, transform_dict, intrinsics_pinhole, intrinsics_pinhole_dict):
    sensor = Sensor(
        uid="rgb_middle",
        extrinsics=transform,
        intrinsics=intrinsics_pinhole,
        type=SensorType.CAMERA,
        uri="/S1206063/image",
    )

    assert sensor.asdict() == {
        "stream": {
            "type": "camera",
            "uri": "/S1206063/image",
            "stream_properties": {
                "intrinsics_pinhole": intrinsics_pinhole_dict
            }
        },
        "coordinate_system": {
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": transform_dict,
        }
    }


def test_radar_fromdict(transform, transform_dict, intrinsics_radar, intrinsics_radar_dict):
    sensor = Sensor.fromdict(
        uid="radar",
        stream_data_dict={
            "type": "radar",
            "uri": "/talker1/Nvt/Cartesian",
            "stream_properties": {
                "intrinsics_radar": intrinsics_radar_dict
            }
        },
        cs_data_dict={
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": transform_dict,
        }
    )

    assert sensor.uid == "radar"
    assert sensor.extrinsics == transform
    assert sensor.intrinsics == intrinsics_radar
    assert sensor.type == SensorType.RADAR
    assert sensor.uri == "/talker1/Nvt/Cartesian"

def test_radar_asdict(transform, transform_dict, intrinsics_radar, intrinsics_radar_dict):
    sensor = Sensor(
        uid="radar",
        extrinsics=transform,
        intrinsics=intrinsics_radar,
        type=SensorType.RADAR,
        uri="/talker1/Nvt/Cartesian",
    )

    assert sensor.asdict() == {
        "stream": {
            "type": "radar",
            "uri": "/talker1/Nvt/Cartesian",
            "stream_properties": {
                "intrinsics_radar": intrinsics_radar_dict
            }
        },
        "coordinate_system": {
            "type": "sensor",
            "parent": "base",
            "pose_wrt_parent": transform_dict,
        }
    }


if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
