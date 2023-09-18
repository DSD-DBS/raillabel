# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import sys
from pathlib import Path
from uuid import UUID

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

import raillabel.format.understand_ai as uai_format
from raillabel._util._warning import _WarningsLogger

# == Fixtures =========================

@pytest.fixture
def frame_uai_dict(
    bounding_box_2d_uai_dict,
    bounding_box_3d_uai_dict,
    polygon_2d_uai_dict,
    polyline_2d_uai_dict,
    segmentation_3d_uai_dict,
    sensor_lidar_uai_dict,
) -> dict:
    return {
        "frameId": "000",
        "timestamp": sensor_lidar_uai_dict["timestamp"],
        "annotations": {
            "2D_BOUNDING_BOX": [bounding_box_2d_uai_dict],
            "2D_POLYLINE": [polyline_2d_uai_dict],
            "2D_POLYGON": [polygon_2d_uai_dict],
            "3D_BOUNDING_BOX": [bounding_box_3d_uai_dict],
            "3D_SEGMENTATION": [segmentation_3d_uai_dict],
        }
    }

@pytest.fixture
def frame_uai(
    bounding_box_2d_uai,
    bounding_box_3d_uai,
    polygon_2d_uai,
    polyline_2d_uai,
    segmentation_3d_uai,
    sensor_lidar_uai,
):
    return uai_format.Frame(
        id=0,
        timestamp=sensor_lidar_uai.timestamp,
        bounding_box_2ds={str(bounding_box_2d_uai.id): bounding_box_2d_uai},
        bounding_box_3ds={str(bounding_box_3d_uai.id): bounding_box_3d_uai},
        polygon_2ds={str(polygon_2d_uai.id): polygon_2d_uai},
        polyline_2ds={str(polyline_2d_uai.id): polyline_2d_uai},
        segmentation_3ds={str(segmentation_3d_uai.id): segmentation_3d_uai},
    )

@pytest.fixture
def frame_raillabel_dict(
    bounding_box_2d_uai, bounding_box_2d_raillabel_dict,
    bounding_box_3d_raillabel_dict,
    polygon_2d_uai, polygon_2d_raillabel_dict,
    polyline_2d_uai, polyline_2d_raillabel_dict,
    segmentation_3d_uai, segmentation_3d_raillabel_dict,
    sensor_lidar_uai, sensor_lidar_raillabel_dict, coordinate_system_lidar_translated_uid,
    sensor_camera_raillabel_dict, coordinate_system_camera_translated_uid,
) -> dict:
    return {
        "frame_properties": {
            "timestamp": str(sensor_lidar_uai.timestamp),
            "streams": {
                coordinate_system_camera_translated_uid: sensor_camera_raillabel_dict,
                coordinate_system_lidar_translated_uid: sensor_lidar_raillabel_dict,
            }
        },
        "objects": {
            str(bounding_box_2d_uai.object_id): {
                "object_data": {
                    "bbox": [bounding_box_2d_raillabel_dict],
                    "cuboid": [bounding_box_3d_raillabel_dict],
                }
            },
            str(polygon_2d_uai.object_id): {
                "object_data": {
                    "poly2d": [polygon_2d_raillabel_dict]
                }
            },
            str(polyline_2d_uai.object_id): {
                "object_data": {
                    "poly2d": [polyline_2d_raillabel_dict]
                }
            },
            str(segmentation_3d_uai.object_id): {
                "object_data": {
                    "vec": [segmentation_3d_raillabel_dict]
                }
            },
        }
    }

# == Tests ============================

def test_fromdict(
    bounding_box_2d_uai_dict, bounding_box_2d_uai,
    bounding_box_3d_uai_dict, bounding_box_3d_uai,
    polygon_2d_uai_dict, polygon_2d_uai,
    polyline_2d_uai_dict, polyline_2d_uai,
    segmentation_3d_uai_dict, segmentation_3d_uai,
    sensor_lidar_uai_dict, sensor_lidar_uai,
):
    frame = uai_format.Frame.fromdict(
        {
            "frameId": "000",
            "timestamp": sensor_lidar_uai_dict["timestamp"],
            "annotations": {
                "2D_BOUNDING_BOX": [bounding_box_2d_uai_dict],
                "2D_POLYLINE": [polyline_2d_uai_dict],
                "2D_POLYGON": [polygon_2d_uai_dict],
                "3D_BOUNDING_BOX": [bounding_box_3d_uai_dict],
                "3D_SEGMENTATION": [segmentation_3d_uai_dict],
            }
        }
    )

    assert frame.id == 0
    assert frame.timestamp == sensor_lidar_uai.timestamp
    assert frame.bounding_box_2ds == {str(bounding_box_2d_uai.id): bounding_box_2d_uai}
    assert frame.bounding_box_3ds == {str(bounding_box_3d_uai.id): bounding_box_3d_uai}
    assert frame.polygon_2ds == {str(polygon_2d_uai.id): polygon_2d_uai}
    assert frame.polyline_2ds == {str(polyline_2d_uai.id): polyline_2d_uai}
    assert frame.segmentation_3ds == {str(segmentation_3d_uai.id): segmentation_3d_uai}


def test_to_raillabel(
    bounding_box_2d_uai, bounding_box_2d_raillabel_dict,
    bounding_box_3d_uai, bounding_box_3d_raillabel_dict,
    polygon_2d_uai, polygon_2d_raillabel_dict,
    polyline_2d_uai, polyline_2d_raillabel_dict,
    segmentation_3d_uai, segmentation_3d_raillabel_dict,
    sensor_lidar_uai, sensor_lidar_raillabel_dict, coordinate_system_lidar_translated_uid,
    sensor_camera_raillabel_dict, coordinate_system_camera_translated_uid,
):
    frame = uai_format.Frame(
        id=0,
        timestamp=sensor_lidar_uai.timestamp,
        bounding_box_2ds={str(bounding_box_2d_uai.id): bounding_box_2d_uai},
        bounding_box_3ds={str(bounding_box_3d_uai.id): bounding_box_3d_uai},
        polygon_2ds={str(polygon_2d_uai.id): polygon_2d_uai},
        polyline_2ds={str(polyline_2d_uai.id): polyline_2d_uai},
        segmentation_3ds={str(segmentation_3d_uai.id): segmentation_3d_uai},
    )

    assert frame.to_raillabel() == {
        "frame_properties": {
            "timestamp": str(sensor_lidar_uai.timestamp),
            "streams": {
                coordinate_system_camera_translated_uid: sensor_camera_raillabel_dict,
                coordinate_system_lidar_translated_uid: sensor_lidar_raillabel_dict,
            }
        },
        "objects": {
            str(bounding_box_2d_uai.object_id): {
                "object_data": {
                    "bbox": [bounding_box_2d_raillabel_dict],
                    "cuboid": [bounding_box_3d_raillabel_dict],
                }
            },
            str(polygon_2d_uai.object_id): {
                "object_data": {
                    "poly2d": [polygon_2d_raillabel_dict]
                }
            },
            str(polyline_2d_uai.object_id): {
                "object_data": {
                    "poly2d": [polyline_2d_raillabel_dict]
                }
            },
            str(segmentation_3d_uai.object_id): {
                "object_data": {
                    "vec": [segmentation_3d_raillabel_dict]
                }
            },
        }
    }


def test_warning_duplicate_annotation_id(
    bounding_box_2d_uai_dict, polyline_2d_uai_dict,
    sensor_lidar_uai_dict
):
    polyline_2d_uai_dict["id"] = bounding_box_2d_uai_dict["id"]

    frame_dict = {
        "frameId": "000",
        "timestamp": sensor_lidar_uai_dict["timestamp"],
        "annotations": {
            "2D_BOUNDING_BOX": [bounding_box_2d_uai_dict],
            "2D_POLYLINE": [polyline_2d_uai_dict],
            "2D_POLYGON": [],
            "3D_BOUNDING_BOX": [],
            "3D_SEGMENTATION": [],
        }
    }

    with _WarningsLogger() as logger:
        uai_format.Frame.fromdict(frame_dict)

    assert len(logger.warnings) == 1
    assert bounding_box_2d_uai_dict["id"] in logger.warnings[0]


if __name__ == "__main__":
    import os
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-vv"])
