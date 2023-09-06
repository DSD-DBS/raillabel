# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

import raillabel
from raillabel.format import annotation_classes

# == Fixtures =========================

@pytest.fixture
def all_annotations(
    bbox, bbox_train,
    cuboid,
    poly2d,
    poly3d,
    seg3d,
):
    return {
        bbox.uid: bbox,
        bbox_train.uid: bbox_train,
        cuboid.uid: cuboid,
        poly2d.uid: poly2d,
        poly3d.uid: poly3d,
        seg3d.uid: seg3d,
    }

# == Tests ============================

def test_post_init_happy(object_person, point2d, size2d):
    raillabel.format.Bbox(
        uid="d2764400-8560-4991-a491-ada598b345c8",
        object=object_person,
        pos=point2d,
        size=size2d,
    )

def test_post_init_unhappy(object_person, point2d):
    with pytest.raises(TypeError):
        raillabel.format.Bbox(
            uid="d2764400-8560-4991-a491-ada598b345c8",
            object=object_person,
            pos=point2d,
        )


def test_annotation_classes():
    assert annotation_classes() == {
        "bbox": raillabel.format.Bbox,
        "poly2d": raillabel.format.Poly2d,
        "cuboid": raillabel.format.Cuboid,
        "poly3d": raillabel.format.Poly3d,
        "vec": raillabel.format.Seg3d,
    }


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear", "-v"])
