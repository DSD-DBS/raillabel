# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import decimal
from dataclasses import dataclass, field

from ._object_annotation import _ObjectAnnotation
from .num import Num
from .sensor_reference import SensorReference


@dataclass
class Frame:
    """A container of dynamic, timewise, information.

    Parameters
    ----------
    timestamp: decimal.Decimal, optional
        Timestamp containing the Unix epoch time of the frame with up to nanosecond precision.
    sensors: dict of raillabel.format.SensorReference, optional
        References to the sensors with frame specific information like timestamp and uri.
        Default is {}.
    frame_data: dict, optional
        Dictionary containing data directly connected to the frame and not to any object, like
        gps/imu data. Dictionary keys are the ID-strings of the variable the data belongs to.
        Default is {}.
    annotations: dict[str, _ObjectAnnotation subclass], optional
        Dictionary containing all annotations of this frame. Keys are annotation uids.

    Read-Only Attributes
    --------------------
    object_data: dict[str, dict[str, _ObjectAnnotation subclass]]
        Annotations categorized by object. Keys are object uids and values are the annotations
        as a dict, that are part of the object.

    """

    timestamp: decimal.Decimal | None = None
    sensors: dict[str, SensorReference] = field(default_factory=dict)
    frame_data: dict[str, Num] = field(default_factory=dict)
    annotations: dict[str, type[_ObjectAnnotation]] = field(default_factory=dict)

    @property
    def object_data(self) -> dict[str, dict[str, type[_ObjectAnnotation]]]:
        """Return annotations categorized by Object-Id.

        Returns
        -------
        dict[str, dict[UUID, _ObjectAnnotation subclass]]
            Dictionary of annotations. Keys are object uids and values are annotations, that are
            contained in the object.

        """
        object_data: dict[str, dict[str, type[_ObjectAnnotation]]] = {}
        for ann_id, annotation in self.annotations.items():
            if annotation.object.uid not in object_data:
                object_data[annotation.object.uid] = {}

            object_data[annotation.object.uid][ann_id] = annotation

        return object_data
