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

        return dict_repr
