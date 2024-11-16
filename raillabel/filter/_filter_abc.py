# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod

from raillabel.format import Frame


class _FilterAbc(ABC):
    """Base class of all filter classes regardless of level."""


class _FrameLevelFilter(_FilterAbc):
    """Base class of all filter classes applied to the frames."""

    @abstractmethod
    def passes_filter(self, frame_id: int, frame: Frame) -> bool:
        """Assess if a frame passes this filter."""
        raise NotImplementedError
