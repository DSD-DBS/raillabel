# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from ._object_annotation import _ObjectAnnotation
from .point3d import Point3d
from .quaternion import Quaternion
from .size3d import Size3d


@dataclass
class Cuboid(_ObjectAnnotation):
    """3D bounding box.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier of the annotation.
    pos: raillabel.format.Point3d
        The center position of the cuboid in meters, where the x coordinate points ahead of the
        vehicle, y points to the left and z points upwards.
    quat: raillabel.format.Quaternion
        The rotation of the cuboid in quaternions.
    size: raillabel.format.Size3d
        The size of the cuboid in meters.
    object: raillabel.format.Object
        A reference to the object, this annotation belongs to.
    sensor: raillabel.format.Sensor
        A reference to the sensor, this annotation is labeled in. Default is None.
    attributes: dict, optional
        Attributes of the annotation. Dict keys are the name str of the attribute, values are the
        attribute values. Default is {}.

    Properties (read-only)
    ----------------------
    name: str
        Name of the annotation used by the VCD player for indexing in the object data pointers.

    """

    pos: Point3d
    quat: Quaternion
    size: Size3d

    OPENLABEL_ID = "cuboid"
