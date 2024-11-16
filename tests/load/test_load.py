# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pytest

import raillabel


def test_load(json_paths):
    actual = raillabel.load(json_paths["openlabel_v1_short"])
    assert len(actual.sensors) == 4
    assert len(actual.objects) == 3
    assert len(actual.frames) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
