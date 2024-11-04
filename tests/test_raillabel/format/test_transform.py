# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

from raillabel.format import Transform
from raillabel.json_format import JSONTransformData


# == Fixtures =========================


@pytest.fixture
def transform_json(point3d_json, quaternion_json) -> JSONTransformData:
    return JSONTransformData(translation=point3d_json, quaternion=quaternion_json)


@pytest.fixture
def transform(point3d, quaternion) -> Transform:
    return Transform(position=point3d, quaternion=quaternion)


# == Tests ============================


def test_from_json(transform_json, transform):
    actual = Transform.from_json(transform_json)
    assert actual == transform


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
