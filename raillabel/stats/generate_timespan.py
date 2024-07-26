# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from decimal import Decimal

from ..format import Scene


def generate_timespan(scene: Scene) -> t.Tuple[t.Optional[Decimal], t.Optional[Decimal]]:
    """Return start and end timestamp of the scene.

    Parameters
    ----------
    scene: raillabel.format.Scene
        Scene the timespan should be based off.

    Returns
    -------
    decimal.Decimal or None
        Start timestamp of the scene. Is None if the scene has no frames.
    decimal.Decimal or None
        End timestamp of the scene. Is None if the scene has no frames.
    """
    start_timestamp = None
    end_timestamp = None

    for frame in scene.frames.values():

        if start_timestamp == None or frame.timestamp < start_timestamp:
            start_timestamp = frame.timestamp

        if end_timestamp == None or frame.timestamp > end_timestamp:
            end_timestamp = frame.timestamp

    return (start_timestamp, end_timestamp)
