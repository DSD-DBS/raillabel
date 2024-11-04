# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Transform
from raillabel.json_format import JSONTransformData


# == Fixtures =========================


@pytest.fixture
def transform_dict(point3d_dict, quaternion_dict) -> dict:
    return {"translation": point3d_dict, "quaternion": quaternion_dict}


@pytest.fixture
def transform_json(point3d_dict, quaternion_dict) -> JSONTransformData:
    return JSONTransformData(translation=point3d_dict, quaternion=quaternion_dict)


@pytest.fixture
def transform(point3d, quaternion) -> Transform:
    return Transform(position=point3d, quaternion=quaternion)


# == Tests ============================


def test_from_json(transform_json, transform):
    actual = Transform.from_json(transform_json)
    assert actual == transform


def test_fromdict(point3d, point3d_dict, quaternion, quaternion_dict):
    transform = Transform.fromdict({"translation": point3d_dict, "quaternion": quaternion_dict})

    assert transform.position == point3d
    assert transform.quaternion == quaternion


def test_asdict(point3d, point3d_dict, quaternion, quaternion_dict):
    transform = Transform(position=point3d, quaternion=quaternion)

    assert transform.asdict() == {"translation": point3d_dict, "quaternion": quaternion_dict}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
