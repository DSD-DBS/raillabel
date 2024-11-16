# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
from .test_attributes import attributes_multiple_types, attributes_multiple_types_json
from .test_bbox import bbox, bbox_json, bbox_id
from .test_camera import camera, camera_json
from .test_cuboid import cuboid, cuboid_json, cuboid_id
from .test_frame import frame, frame_json
from .test_frame_interval import frame_interval, frame_interval_json
from .test_intrinsics_pinhole import intrinsics_pinhole, intrinsics_pinhole_json
from .test_intrinsics_radar import intrinsics_radar, intrinsics_radar_json
from .test_lidar import lidar, lidar_json
from .test_metadata import metadata, metadata_json
from .test_num import num, num_json, num_id
from .test_object import (
    objects,
    object_person,
    object_person_json,
    object_person_id,
    object_track,
    object_track_json,
    object_track_id,
)
from .test_point2d import point2d, point2d_json, another_point2d, another_point2d_json
from .test_point3d import point3d, point3d_json, another_point3d, another_point3d_json
from .test_poly2d import poly2d, poly2d_json, poly2d_id
from .test_poly3d import poly3d, poly3d_json, poly3d_id
from .test_quaternion import quaternion, quaternion_json
from .test_radar import radar, radar_json
from .test_size2d import size2d, size2d_json
from .test_size3d import size3d, size3d_json
from .test_seg3d import seg3d, seg3d_json, seg3d_id
from .test_sensor_reference import (
    another_sensor_reference,
    another_sensor_reference_json,
    sensor_reference,
    sensor_reference_json,
)
from .test_transform import transform, transform_json
