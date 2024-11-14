# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ._json_format_base import _JSONFormatBase


class JSONFrameInterval(_JSONFormatBase):
    """A frame interval defines a starting and ending frame number as a closed interval.

    That means the interval includes the limit frame numbers.
    """

    frame_start: int
    "Initial frame number of the interval."

    frame_end: int
    "Ending frame number of the interval."
