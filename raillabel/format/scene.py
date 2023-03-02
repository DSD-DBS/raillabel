# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
import uuid
from dataclasses import dataclass, field

from .frame import Frame
from .metadata import Metadata
from .object import Object
from .sensor import Sensor


@dataclass
class Scene:
    """The root RailLabel class, which contains all data.

    Parameters
    ----------
    metadata: raillabel.format.Metadata
        This object contains information, that is, metadata, about the annotation file itself.
    sensors: dict of raillabel.format.Sensor, optional
        Dictionary of raillabel.format.Sensors. Dictionary keys are the sensor uids. Default is {}.
    objects: dict of raillabel.format.Object, optional
        Dictionary of raillabel.format.Objects. Dictionary keys are the object uids. Default is {}.
    frames: dict of raillabel.format.Frame, optional
        Dict of frames in the scene. Dictionary keys are the frame uids. Default is {}.
    """

    metadata: Metadata
    sensors: t.Dict[str, Sensor] = field(default_factory=dict)
    objects: t.Dict[uuid.UUID, Object] = field(default_factory=dict)
    frames: t.Dict[int, Frame] = field(default_factory=dict)

    def asdict(self) -> dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this Scene.

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.
        """

        dict_repr = {"openlabel": {"metadata": self.metadata.asdict()}}

        if self.sensors != {}:
            dict_repr["openlabel"]["streams"] = {
                str(k): v.asdict()["stream"] for k, v in self.sensors.items()
            }
            dict_repr["openlabel"]["coordinate_systems"] = {
                str(k): v.asdict()["coordinate_system"] for k, v in self.sensors.items()
            }
            dict_repr["openlabel"]["coordinate_systems"]["base"] = {
                "type": "local",
                "parent": "",
                "children": list(self.sensors.keys()),
            }

        if self.objects != {}:
            dict_repr["openlabel"]["objects"] = {
                str(k): v.asdict() for k, v in self.objects.items()
            }

        if self.frames != {}:
            dict_repr["openlabel"]["frames"] = {str(k): v.asdict() for k, v in self.frames.items()}

        dict_repr = self._add_object_data_pointers(dict_repr)

        return dict_repr

    def _add_object_data_pointers(self, dict_repr: dict) -> dict:
        """Add object frame intervals and object_data_pointers to the JSON.

        The VCD visualization tool requires a short "summary" of where an object and the
        object_data_pointers occurr, which includes the frame intervals of the object and the frame
        intervals of the object_data names.

        Parameters
        ----------
        dict_repr : dict
            Dictionary in the OpenLABEL format, that should be enhanced.

        Returns
        -------
        dict
            Enhanced dictionary.
        """

        # Creates the frame intervals and object_data_pointers
        frame_intervals = []
        object_frame_intervals = {}
        for frame in self.frames.values():

            # Adds the frame intervals
            if len(frame_intervals) == 0:
                frame_intervals.append(
                    {
                        "frame_start": frame.uid,
                        "frame_end": frame.uid,
                    }
                )

            elif frame.uid == frame_intervals[-1]["frame_end"] + 1:
                frame_intervals[-1]["frame_end"] += 1

            else:
                frame_intervals.append(
                    {
                        "frame_start": frame.uid,
                        "frame_end": frame.uid,
                    }
                )

            # Adds the object frame intervals
            for object_id in frame.object_data:

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
            for object_id in frame.object_data:
                for annotation in frame.object_data[object_id].annotations.values():

                    if (
                        annotation.name
                        not in object_frame_intervals[object_id]["object_data_pointers"]
                    ):
                        object_frame_intervals[object_id]["object_data_pointers"][
                            annotation.name
                        ] = {
                            "type": annotation.name.split("__")[1],
                            "frame_intervals": [
                                {
                                    "frame_start": frame.uid,
                                    "frame_end": frame.uid,
                                }
                            ],
                            "attribute_pointers": {},
                        }

                    else:
                        if (
                            object_frame_intervals[object_id]["object_data_pointers"][
                                annotation.name
                            ]["frame_intervals"][-1]["frame_end"]
                            >= frame.uid - 1
                        ):
                            object_frame_intervals[object_id]["object_data_pointers"][
                                annotation.name
                            ]["frame_intervals"][-1]["frame_end"] = frame.uid

                        else:
                            object_frame_intervals[object_id]["object_data_pointers"][
                                annotation.name
                            ]["frame_intervals"].append(
                                {
                                    "frame_start": frame.uid,
                                    "frame_end": frame.uid,
                                }
                            )

                    for attr_name, attr_value in annotation.attributes.items():

                        if type(attr_value) == str:
                            attr_type = "text"

                        elif type(attr_value) in [float, int]:
                            attr_type = "num"

                        elif type(attr_value) == bool:
                            attr_type = "boolean"

                        elif type(attr_value) in [list, tuple]:
                            attr_type = "vec"

                        object_frame_intervals[object_id]["object_data_pointers"][annotation.name][
                            "attribute_pointers"
                        ][attr_name] = attr_type

        # Adds the frame_intervals to the dict
        dict_repr["openlabel"]["frame_intervals"] = frame_intervals

        # Adds the object_data_pointers to the dict
        if "objects" in dict_repr["openlabel"]:
            for object_id, object in dict_repr["openlabel"]["objects"].items():
                object.update(object_frame_intervals[object_id])

        return dict_repr
