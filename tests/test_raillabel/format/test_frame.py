# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from decimal import Decimal

import pytest

from raillabel.format import Frame
from raillabel.json_format import JSONFrame, JSONFrameData, JSONFrameProperties, JSONObjectData

# == Fixtures =========================


@pytest.fixture
def frame_json(
    sensor_reference_json,
    another_sensor_reference_json,
    num_json,
    bbox_json,
    cuboid_json,
    poly2d_json,
    poly3d_json,
    seg3d_json,
) -> JSONFrame:
    return JSONFrame(
        frame_properties=JSONFrameProperties(
            timestamp=Decimal("1631337747.123123123"),
            streams={
                "rgb_middle": sensor_reference_json,
                "lidar": another_sensor_reference_json,
            },
            frame_data=JSONFrameData(num=[num_json]),
        ),
        objects={
            "cfcf9750-3bc3-4077-9079-a82c0c63976a": JSONObjectData(
                poly2d=[poly2d_json],
                poly3d=[poly3d_json],
            ),
            "b40ba3ad-0327-46ff-9c28-2506cfd6d934": JSONObjectData(
                bbox=[bbox_json],
                cuboid=[cuboid_json],
                vec=[seg3d_json],
            ),
        },
    )


@pytest.fixture
def frame(
    sensor_reference,
    another_sensor_reference,
    num,
    bbox,
    bbox_id,
    cuboid,
    cuboid_id,
    poly2d,
    poly2d_id,
    poly3d,
    poly3d_id,
    seg3d,
    seg3d_id,
) -> dict:
    return Frame(
        timestamp=Decimal("1631337747.123123123"),
        sensors={
            "rgb_middle": sensor_reference,
            "lidar": another_sensor_reference,
        },
        frame_data={num.name: num},
        annotations={
            bbox_id: bbox,
            cuboid_id: cuboid,
            poly2d_id: poly2d,
            poly3d_id: poly3d,
            seg3d_id: seg3d,
        },
    )


# == Tests ============================


def test_from_json(frame, frame_json):
    actual = Frame.from_json(frame_json)
    assert actual == frame


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
