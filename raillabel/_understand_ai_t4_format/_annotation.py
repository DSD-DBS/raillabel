# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from .sensor_reference import SensorReference


@dataclass
class _Annotation(ABC):

    id: UUID
    object_id: UUID
    class_name: str
    attributes: dict
    sensor: SensorReference

    @classmethod
    @abstractmethod
    def fromdict(cls, data_dict: t.Dict) -> t.Type["_Annotation"]:
        raise NotImplementedError
