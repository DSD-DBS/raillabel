# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from .test_attributes import (
    attributes_multiple_types,
    attributes_multiple_types_dict,
    attributes_single_type,
    attributes_single_type_dict,
)
from .test_bbox import bbox, bbox_dict, bbox_train, bbox_train_dict
from .test_cuboid import cuboid, cuboid_dict
from .test_element_data_pointer import (
    element_data_pointer_full,
    element_data_pointer_full_dict,
    element_data_pointer_minimal,
    element_data_pointer_minimal_dict,
)
from .test_frame import frame, frame_dict
from .test_frame_interval import frame_interval, frame_interval_dict
from .test_intrinsics_pinhole import intrinsics_pinhole, intrinsics_pinhole_dict
from .test_intrinsics_radar import intrinsics_radar, intrinsics_radar_dict
from .test_metadata import (
    metadata_full,
    metadata_full_dict,
    metadata_minimal,
    metadata_minimal_dict,
)
from .test_num import num, num_dict
from .test_object import (
    object_person,
    object_person_dict,
    object_train,
    object_train_dict,
    objects,
    objects_dict,
)
from .test_object_annotation import all_annotations
from .test_object_data import object_data_person_dict, object_data_train_dict
from .test_point2d import point2d, point2d_another, point2d_another_dict, point2d_dict
from .test_point3d import point3d, point3d_another, point3d_another_dict, point3d_dict
from .test_poly2d import poly2d, poly2d_dict
from .test_poly3d import poly3d, poly3d_dict
from .test_quaternion import quaternion, quaternion_dict
from .test_scene import scene, scene_dict
from .test_seg3d import seg3d, seg3d_dict
from .test_sensor import (
    coordinate_systems_dict,
    sensor_camera,
    sensor_camera_dict,
    sensor_lidar,
    sensor_lidar_dict,
    sensor_radar,
    sensor_radar_dict,
    sensors,
    streams_dict,
)
from .test_sensor_reference import sensor_reference_camera, sensor_reference_camera_dict
from .test_size2d import size2d, size2d_dict
from .test_size3d import size3d, size3d_dict
from .test_transform import transform, transform_dict
