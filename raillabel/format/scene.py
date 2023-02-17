# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
import uuid
from dataclasses import dataclass, field

from .coordinate_system import CoordinateSystem
from .frame import Frame
from .metadata import Metadata
from .object import Object
from .stream import Stream


@dataclass
class Scene:
    """The root RailLabel class, which contains all data.

    Parameters
    ----------
    metadata: raillabel.format.Metadata
        This object contains information, that is, metadata, about the annotation file itself.
    streams: dict of raillabel.format.Stream, optional
        Dictionary of raillabel.format.Streams. Dictionary keys are the stream uids. Default is {}.
    coordinate_systems: dict of raillabel.format.CoordinateSystem, optional
        Dictionary of raillabel.format.CoordinateSystems. Dictionary keys are the coordinate_system
        uids. Default is {}.
    objects: dict of raillabel.format.Object, optional
        Dictionary of raillabel.format.Objects. Dictionary keys are the object uids. Default is {}.
    frames: dict of raillabel.format.Frame, optional
        Dict of frames in the scene. Dictionary keys are the frame uids. Default is {}.
    """

    metadata: Metadata
    streams: t.Dict[str, Stream] = field(default_factory=dict)
    coordinate_systems: t.Dict[str, CoordinateSystem] = field(default_factory=dict)
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

        if self.streams != {}:
            dict_repr["openlabel"]["streams"] = {
                str(k): v.asdict() for k, v in self.streams.items()
            }

        if self.coordinate_systems != {}:
            dict_repr["openlabel"]["coordinate_systems"] = {
                str(k): v.asdict() for k, v in self.coordinate_systems.items()
            }

        if self.objects != {}:
            dict_repr["openlabel"]["objects"] = {
                str(k): v.asdict() for k, v in self.objects.items()
            }

        if self.frames != {}:
            dict_repr["openlabel"]["frames"] = {str(k): v.asdict() for k, v in self.frames.items()}

        return dict_repr
