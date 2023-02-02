# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from decimal import Decimal

from .format.scene import Scene


def filter(
    scene: Scene,
    include_annotation_ids: t.List[str] = [],
    exclude_annotation_ids: t.List[str] = [],
    include_annotation_types: t.List[str] = [],
    exclude_annotation_types: t.List[str] = [],
    include_attributes: dict = {},
    exclude_attributes: dict = {},
    include_classes: t.List[str] = [],
    exclude_classes: t.List[str] = [],
    include_frames: t.List[int] = [],
    exclude_frames: t.List[int] = [],
    start_frame: int = -1,
    end_frame: int = float("inf"),
    start_timestamp: Decimal = -1,
    end_timestamp: Decimal = float("inf"),
    include_object_ids: t.List[str] = [],
    exclude_object_ids: t.List[str] = [],
    include_sensors: t.List[str] = [],
    exclude_sensors: t.List[str] = [],
) -> Scene:
    """Return a copy of the scene with the annotations filtered.

    Parameters
    ----------
    scene: raillabel.Scene
        Scene, which should be copied and filtered.
    include_classes: str or list of str
        List of class/type names that should be included in the filtered scene. If set, no
        other classes/types will be copied. Mutually exclusive with exclude_classes.
    exclude_classes: str or list of str
        List of class/type names that should be excluded in the filtered scene. If set, all
        other classes/types will be copied. Mutually exclusive with include_classes.
    include_annotation_types: str or list of str
        List of annotation types (i.e. bboxs, cuboids, poly2ds, seg3ds) that should be included
        in the filtered scene. If set, no other annotation types will be copied. Mutually
        exclusive with exclude_annotation_types.
    exclude_annotation_types: str or list of str
        List of annotation types (i.e. bboxs, cuboids, poly2ds, seg3ds) that should be excluded
        in the filtered scene. If set, all other annotation types will be copied. Mutually
        exclusive with include_annotation_types.
    include_annotation_ids: str or list of str
        List of annotation UIDs that should be included in the filtered scene. If set, no other
        annotation UIDs will be copied. Mutually exclusive with exclude_annotation_ids.
    exclude_annotation_ids: str or list of str
        List of annotation UIDs that should be excluded in the filtered scene. If set, all
        other annotation UIDs will be copied. Mutually exclusive with include_annotation_ids.
    include_object_ids: str or list of str
        List of object UIDs that should be included in the filtered scene. If set, no other
        objects will be copied. Mutually exclusive with exclude_object_ids.
    exclude_object_ids: str or list of str
        List of object UIDs that should be excluded in the filtered scene. If set, all other
        objects will be copied. Mutually exclusive with include_object_ids.
    include_sensors: str or list of str
        List of sensors that should be included in the filtered scene. If set, no other
        sensors will be copied. Mutually exclusive with exclude_sensors.
    exclude_sensors: str or list of str
        List of sensors that should be excluded in the filtered scene. If set, all other
        sensors will be copied. Mutually exclusive with include_sensors.
    include_attributes: dict
        Dict of attributes that should be included in the filtered scene. Dict keys are the
        attribute names, values are the specific values that should be included. If the
        value is set so None, all annotations with the attribute are included regardless of
        value. Mutually exclusive with exclude_attributes.
    exclude_attributes: dict
        Dict of attributes that should be excluded in the filtered scene. Dict keys are the
        attribute names, values are the specific values that should be excluded. If the value
        is set so None, all annotations with the attribute are excluded regardless of value.
        Mutually exclusive with include_attributes.
    include_frames: int or list of int
        List of frame UIDs that should be included in the filtered scene. If set, no other
        frames will be copied. Mutually exclusive with exclude_frames.
    exclude_frames: int or list of int
        List of frame UIDs that should be excluded in the filtered scene. If set, all other
        frames will be copied. Mutually exclusive with include_frames.
    start_frame: int
        Frame at which the filtered scene should start. Mutually exclusive with s
        tart_timestamp.
    end_frame: int
        Frame at which the filtered scene should end (inclusive). Mutually exclusive with
        end_timestamp.
    start_timestamp: decimal.Decimal
        Unix timestamp at which the filtered scene should start (inclusive). Mutually exclusive
        with start_frame.
    end_timestamp: decimal.Decimal
        Unix timestamp at which the filtered scene should end (inclusive). Mutually exclusive
        with end_frame.

    Raises
    ------
    ValueError
        if two mutually exclusive parameters are set.
    """

    return scene.filter(
        include_annotation_ids,
        exclude_annotation_ids,
        include_annotation_types,
        exclude_annotation_types,
        include_attributes,
        exclude_attributes,
        include_classes,
        exclude_classes,
        include_frames,
        exclude_frames,
        start_frame,
        end_frame,
        start_timestamp,
        end_timestamp,
        include_object_ids,
        exclude_object_ids,
        include_sensors,
        exclude_sensors,
    )
