# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import pickle
import typing as t

from . import _filter_classes, format


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

    filtered_scene = _copy(scene)

    used_sensors = set()
    used_objects = set()

    for frame_id, frame in scene.frames.items():

        if not _passes_filters(frame, filters_by_level["frame"]):
            del filtered_scene.frames[frame_id]
            continue

        for frame_data_id, frame_data in frame.frame_data.items():

            if _passes_filters(frame_data, filters_by_level["frame_data"]):
                used_sensors.add(frame_data.sensor.uid)

            else:
                del filtered_scene.frames[frame_id].frame_data[frame_data_id]

        for object_id, object_data in frame.object_data.items():

            if not _passes_filters(scene.objects[object_id], filters_by_level["object"]):
                continue

            for annotation_id, annotation in object_data.annotations.items():

                if _passes_filters(annotation, filters_by_level["annotation"]):
                    used_objects.add(object_id)
                    used_sensors.add(annotation.sensor.uid)

                else:
                    del (
                        filtered_scene.frames[frame_id]
                        .object_data[object_id]
                        .annotations[annotation_id]
                    )

    # Clears out any unused sensors, objects and references

    for sensor_id in scene.sensors:
        if sensor_id not in used_sensors:
            del filtered_scene.sensors[sensor_id]

    for object_id in scene.objects:
        if object_id not in used_objects:
            del filtered_scene.objects[object_id]

    for frame_id in filtered_scene.frames:

        for sensor_id in scene.frames[frame_id].sensors:
            if sensor_id not in used_sensors:
                del filtered_scene.frames[frame_id].sensors[sensor_id]

        for object_id in scene.frames[frame_id].object_data:

            if (
                object_id not in used_objects
                or len(filtered_scene.frames[frame_id].object_data[object_id].annotations) == 0
            ):
                del filtered_scene.frames[frame_id].object_data[object_id]

    return filtered_scene


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
        for filter in filters:
            if level in filter.LEVELS:
                filters_by_level[level].append(filter)

    return filters_by_level


def _passes_filters(data, filters):
    for f in filters:
        if not f.passes_filter(data):
            return False

    return True


def _copy(object):
    return pickle.loads(pickle.dumps(object, -1))
