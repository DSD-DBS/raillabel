# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from ._object_annotation import _ObjectAnnotation


@dataclass
class Seg3d(_ObjectAnnotation):
    """The 3D segmentation of a lidar pointcloud.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier of the annotation.
    point_ids: list of int
        The list of point indices.
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

    point_ids: list[int]

    OPENLABEL_ID = "vec"
