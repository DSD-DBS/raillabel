# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass, field

from .camera import Camera
from .frame import Frame
from .frame_interval import FrameInterval
from .metadata import Metadata
from .object import Object
from .radar import Radar


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

    Properties (read-only)
    ----------------------
    frame_intervals: list[FrameIntervals]
        List of frame intervals describing the frames present in this scene.

    """

    metadata: Metadata
    sensors: dict[str, Camera | Radar] = field(default_factory=dict)
    objects: dict[str, Object] = field(default_factory=dict)
    frames: dict[int, Frame] = field(default_factory=dict)

    @property
    def frame_intervals(self) -> list[FrameInterval]:
        """Return frame intervals of the present frames."""
        return FrameInterval.from_frame_uids(list(self.frames.keys()))
