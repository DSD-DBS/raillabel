# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from .point2d import Point2d
from .size2d import Size2d


@dataclass
class Bbox:
    """A 2D bounding box in an image.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier of the annotation.
    pos: raillabel.format.Point2d
        The center point of the bbox in pixels.
    size: raillabel.format.Size2d
        The dimensions of the bbox in pixels from the top left corner to the bottom right corner.
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

    pos: Point2d
    "The center point of the bbox in pixels."

    size: Size2d
    "The dimensions of the bbox in pixels from the top left corner to the bottom right corner."

    object: UUID
    "The uid of the object, this annotation belongs to."

    sensor: str
    "The uid of the sensor, this annotation is labeled in."

    attributes: dict[str, int | float | bool | str | list]
