# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import pickle
import typing as t

from .. import format
from . import _filter_classes


def filter(scene: format.Scene, **kwargs) -> format.Scene:
    """Return a copy of the scene with the annotations filtered.

    Parameters
    ----------
    scene: raillabel.Scene
        Scene, which should be copied and filtered.
    include_object_types: str or list of str, optional
        List of class/type names that should be included in the filtered scene. If set, no
        other classes/types will be copied. Mutually exclusive with exclude_object_types.
    exclude_object_types: str or list of str, optional
        List of class/type names that should be excluded in the filtered scene. If set, all
        other classes/types will be copied. Mutually exclusive with include_object_types.
    include_annotation_types: str or list of str, optional
        List of annotation types (i.e. bboxs, cuboids, poly2ds, seg3ds) that should be included
        in the filtered scene. If set, no other annotation types will be copied. Mutually
        exclusive with exclude_annotation_types.
    exclude_annotation_types: str or list of str, optional
        List of annotation types (i.e. bboxs, cuboids, poly2ds, seg3ds) that should be excluded
        in the filtered scene. If set, all other annotation types will be copied. Mutually
        exclusive with include_annotation_types.
    include_annotation_ids: str or list of str, optional
        List of annotation UIDs that should be included in the filtered scene. If set, no other
        annotation UIDs will be copied. Mutually exclusive with exclude_annotation_ids.
    exclude_annotation_ids: str or list of str, optional
        List of annotation UIDs that should be excluded in the filtered scene. If set, all
        other annotation UIDs will be copied. Mutually exclusive with include_annotation_ids.
    include_object_ids: str or list of str, optional
        List of object UIDs that should be included in the filtered scene. If set, no other
        objects will be copied. Mutually exclusive with exclude_object_ids.
    exclude_object_ids: str or list of str, optional
        List of object UIDs that should be excluded in the filtered scene. If set, all other
        objects will be copied. Mutually exclusive with include_object_ids.
    include_sensors: str or list of str
        List of sensors that should be included in the filtered scene. If set, no other
        sensors will be copied. Mutually exclusive with exclude_sensors.
    exclude_sensors: str or list of str, optional
        List of sensors that should be excluded in the filtered scene. If set, all other
        sensors will be copied. Mutually exclusive with include_sensors.
    include_attributes: dict, optional
        Dict of attributes that should be included in the filtered scene. Dict keys are the
        attribute names, values are the specific values that should be included. If the
        value is set so None, all annotations with the attribute are included regardless of
        value. Mutually exclusive with exclude_attributes.
    exclude_attributes: dict, optional
        Dict of attributes that should be excluded in the filtered scene. Dict keys are the
        attribute names, values are the specific values that should be excluded. If the value
        is set so None, all annotations with the attribute are excluded regardless of value.
        Mutually exclusive with include_attributes.
    include_frames: int or list of int, optional
        List of frame UIDs that should be included in the filtered scene. If set, no other
        frames will be copied. Mutually exclusive with exclude_frames.
    exclude_frames: int or list of int, optional
        List of frame UIDs that should be excluded in the filtered scene. If set, all other
        frames will be copied. Mutually exclusive with include_frames.
    start_frame: int, optional
        Frame at which the filtered scene should start. Mutually exclusive with s
        tart_timestamp.
    end_frame: int, optional
        Frame at which the filtered scene should end (inclusive). Mutually exclusive with
        end_timestamp.
    start_timestamp: decimal.Decimal, optional
        Unix timestamp at which the filtered scene should start (inclusive). Mutually exclusive
        with start_frame.
    end_timestamp: decimal.Decimal, optional
        Unix timestamp at which the filtered scene should end (inclusive). Mutually exclusive
        with end_frame.

    Raises
    ------
    ValueError
        if two mutually exclusive parameters are set.
    TypeError
        if an unexpected keyword argument has been set.
    """

    filters_by_level = _collect_filter_classes(kwargs)
    filtered_scene, used_sensors, used_objects = _filter_scene(_copy(scene), filters_by_level)
    filtered_scene = _remove_unused(filtered_scene, used_sensors, used_objects)

    return filtered_scene


# --- Prepare filter classes


def _collect_filter_classes(kwargs) -> t.Tuple[t.List[t.Type], t.List[str]]:
    filters = []
    supported_kwargs = []
    for cls in _filter_classes.__dict__.values():
        if (
            isinstance(cls, type)
            and issubclass(cls, _filter_classes._FilterABC)
            and cls != _filter_classes._FilterABC
        ):
            filters.append(cls(kwargs))
            supported_kwargs.extend(cls.PARAMETERS)

    _check_for_unsupported_arg(kwargs, supported_kwargs)

    return _seperate_filters_by_level(filters)


def _check_for_unsupported_arg(kwargs: t.List[str], supported_kwargs: t.List[str]):
    for arg in kwargs:
        if arg not in supported_kwargs:
            raise TypeError(
                f"filter() got an unexpected keyword argument '{arg}'. Supported keyword "
                + f"arguments: {sorted(supported_kwargs)}"
            )


def _seperate_filters_by_level(filters: t.List[t.Type]) -> t.Dict[str, t.List[t.Type]]:
    all_filter_levels = [level for f in filters for level in f.LEVELS]

    filters_by_level = {level: [] for level in all_filter_levels}
    for level in filters_by_level:
        for filter_class in filters:
            if level in filter_class.LEVELS:
                filters_by_level[level].append(filter_class)

    return filters_by_level


# --- Filter scene


def _filter_scene(
    scene: format.Scene, filters_by_level: t.Dict[str, t.List[t.Type]]
) -> t.Tuple[format.Scene, t.Set[str], t.Set[str]]:

    used_sensors = set()
    used_objects = set()

    for frame_id, frame in list(scene.frames.items()):

        if not _passes_filters(frame, filters_by_level["frame"]):
            del scene.frames[frame_id]
            continue

        for frame_data_id, frame_data in list(frame.frame_data.items()):

            if _passes_filters(frame_data, filters_by_level["frame_data"]):
                used_sensors.add(frame_data.sensor.uid)

            else:
                del scene.frames[frame_id].frame_data[frame_data_id]

        for annotation_id, annotation in list(frame.annotations.items()):

            if _passes_filters(annotation, filters_by_level["annotation"]):
                used_objects.add(annotation.object.uid)
                used_sensors.add(annotation.sensor.uid)

            else:
                del scene.frames[frame_id].annotations[annotation_id]

    return scene, used_sensors, used_objects


# --- Remove unused


def _remove_unused(
    scene: format.Scene, used_sensors: t.Set[str], used_objects: t.Set[str]
) -> format.Scene:

    scene = _remove_unused_sensors(scene, used_sensors)
    scene = _remove_unused_objects(scene, used_objects)

    for frame_id in scene.frames:

        scene.frames[frame_id] = _remove_unused_sensor_references(
            scene.frames[frame_id], used_sensors
        )

    return scene


def _remove_unused_sensors(scene: format.Scene, used_sensors: t.Set[str]) -> format.Scene:
    for sensor_id in list(scene.sensors):
        if sensor_id not in used_sensors:
            del scene.sensors[sensor_id]

    return scene


def _remove_unused_objects(scene: format.Scene, used_objects: t.Set[str]) -> format.Scene:
    for object_id in list(scene.objects):
        if object_id not in used_objects:
            del scene.objects[object_id]

    return scene


def _remove_unused_sensor_references(frame: format.Frame, used_sensors: t.Set[str]) -> format.Frame:
    for sensor_id in list(frame.sensors):
        if sensor_id not in used_sensors:
            del frame.sensors[sensor_id]

    return frame


# --- Helper functions


def _passes_filters(data, filters):
    for f in filters:
        if not f.passes_filter(data):
            return False

    return True


def _copy(object):
    return pickle.loads(pickle.dumps(object, -1))
