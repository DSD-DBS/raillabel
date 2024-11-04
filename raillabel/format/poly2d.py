# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass

from ._object_annotation import _ObjectAnnotation
from .point2d import Point2d


@dataclass
class Poly2d(_ObjectAnnotation):
    """Sequence of 2D points. Can either be a polygon or polyline.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier for the annotation.
    points: list of raillabel.format.Point2d
        List of the 2d points that make up the polyline.
    closed: bool
        This parameter states, whether the polyline represents a closed shape (a polygon) or an
        open line.
    mode: str, optional
        Mode of the polyline list of values: "MODE_POLY2D_ABSOLUTE" determines that the poly2d list
        contains the sequence of (x, y) values of all points of the polyline. "MODE_POLY2D_RELATIVE"
        specifies that only the first point of the sequence is defined with its (x, y) values, while
        all the rest are defined relative to it. "MODE_POLY2D_SRF6DCC" specifies that SRF6DCC chain
        code method is used. "MODE_POLY2D_RS6FCC" specifies that the RS6FCC method is used. Default
        is 'MODE_POLY2D_ABSOLUTE'.
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

    points: list[Point2d]
    closed: bool
    mode: str = "MODE_POLY2D_ABSOLUTE"

    OPENLABEL_ID = "poly2d"
