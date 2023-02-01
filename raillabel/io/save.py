# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
from pathlib import Path

from .. import exceptions
from ..format import Scene
from .validate import validate as validate_func


def save(scene: Scene, path: str, prettify_json: bool = False, validate: bool = False):
    """Save a raillabel.Scene in a JSON file.

    Parameters
    ----------
    scene: raillabel.Scene
        Scene, which should be saved.
    path: str
        Path to the file location, that should be used for saving.
    save_path: str
        Path to the JSON file.
    quiet: bool, optional
        If true, only minimal console output is produced. Default is True.
    prettify_json: bool, optional
        If true, the JSON is saved with linebreaks and indents. This increases readibility but
        also the file size. Default is False.
    validate: bool, optional
        If True, the annotation data is validated via the OpenLabel schema. This is highly
        recommended, as not validating the data may lead to Errors during loading or while handling
        the scene. However, validating may increase the loading time. Default is False.

    Raises
    ------
    SchemaError
        If the data does not validate via the OpenLabel schema.
    FileNotFoundError
        If the save_path does not point to an accessible file.
    """

    path = Path(path)

    # Converts the data stored in the scene into a dictionary
    data = scene.asdict()

    # The VCD visualization tool requires a short "summary" of where an object and the
    # object_data_pointers occurr, which includes the frame intervals of the object and the frame
    # intervals of the object_data names. This is not implemented in the raillabel.format.Scene,
    # since any changes to the frames might make the summary outdated. Therefore, it is only added
    # at the export step so that the saved files can be used in the visualizer.
    data = _add_object_data_pointers(data, scene)

    # Validates the data
    if validate:
        is_data_valid, err_msgs = validate_func(data)
        if not is_data_valid:
            schema_err_msg = (
                "The data could not be saved, because it does not validate "
                "against the OpenLabel schema:"
            )

            for err_msg in err_msgs:
                schema_err_msg += "\n - " + err_msg

            raise exceptions.SchemaError(schema_err_msg)

    # Saves the data
    with path.open("w") as save_file:

        if prettify_json:
            json.dump(data, save_file, indent=4)
        else:
            json.dump(data, save_file)


def _add_object_data_pointers(data: dict, scene: Scene) -> dict:
    """Add object frame intervals and object_data_pointers to the JSON-data.

    Parameters
    ----------
    data : dict
        Dictionary in the OpenLABEL format, that should be enhanced.
    scene : raillabel.format.Scene
        Scene corresponding to the data.

    Returns
    -------
    dict
        Enhanced dictionary.
    """

    # Creates the frame intervals and object_data_pointers
    object_frame_intervals = {}
    for frame in scene.frames.values():

        # Adds the frame intervals
        for object_id in frame.objects:

            if object_id not in object_frame_intervals:
                object_frame_intervals[object_id] = {
                    "frame_intervals": [
                        {
                            "frame_start": frame.uid,
                            "frame_end": frame.uid,
                        }
                    ],
                    "object_data_pointers": {},
                }

            else:
                if (
                    object_frame_intervals[object_id]["frame_intervals"][-1]["frame_end"]
                    == frame.uid - 1
                ):
                    object_frame_intervals[object_id]["frame_intervals"][-1][
                        "frame_end"
                    ] = frame.uid

                else:
                    object_frame_intervals[object_id]["frame_intervals"].append(
                        {
                            "frame_start": frame.uid,
                            "frame_end": frame.uid,
                        }
                    )

        # Adds the object_data_pointers
        for annotation in frame.annotations.values():

            object_id = annotation.object_annotations.object.uid

            if annotation.name not in object_frame_intervals[object_id]["object_data_pointers"]:
                object_frame_intervals[object_id]["object_data_pointers"][annotation.name] = {
                    "frame_intervals": [
                        {
                            "frame_start": frame.uid,
                            "frame_end": frame.uid,
                        }
                    ]
                }

            else:
                if (
                    object_frame_intervals[object_id]["object_data_pointers"][annotation.name][
                        "frame_intervals"
                    ][-1]["frame_end"]
                    >= frame.uid - 1
                ):
                    object_frame_intervals[object_id]["object_data_pointers"][annotation.name][
                        "frame_intervals"
                    ][-1]["frame_end"] = frame.uid

                else:
                    object_frame_intervals[object_id]["object_data_pointers"][annotation.name][
                        "frame_intervals"
                    ].append(
                        {
                            "frame_start": frame.uid,
                            "frame_end": frame.uid,
                        }
                    )

    # Adds the object_data_pointers to the dict
    for object_id, object in data["openlabel"]["objects"].items():
        object.update(object_frame_intervals[object_id])

    return data
