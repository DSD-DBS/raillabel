# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from uuid import UUID

from ..._util._attribute_type import AttributeType
from ._translation import translate_class_id, translate_sensor_id
from .sensor_reference import SensorReference


@dataclass
class _Annotation(ABC):

    id: UUID
    object_id: UUID
    class_name: str
    attributes: dict
    sensor: SensorReference

    @property
    @abstractproperty
    def OPENLABEL_ID(self) -> t.List[str]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def fromdict(cls, data_dict: t.Dict) -> t.Type["_Annotation"]:
        raise NotImplementedError

    def to_raillabel(self) -> t.Tuple[dict, str, str, dict]:
        """Convert to a raillabel compatible dict.

        Returns
        -------
        annotation: dict
            Dictionary valid for the raillabel schema.
        object_id: str
            Friendly identifier of the object this annotation belongs to.
        class_name: str
            Friendly identifier of the class the annotated object belongs to.
        sensor_reference: dict
            Dictionary of the sensor reference.
        """

        return (
            {
                "name": str(self.id),
                "val": self._val_to_raillabel(),
                "coordinate_system": translate_sensor_id(self.sensor.type),
                "attributes": self._attributes_to_raillabel(),
            },
            str(self.object_id),
            translate_class_id(self.class_name),
            self.sensor.to_raillabel()[1],
        )

    def _attributes_to_raillabel(self) -> dict:

        attributes = {}

        for attr_name, attr_value in self.attributes.items():

            attr_type = AttributeType.from_value(type(attr_value)).value

            if attr_type not in attributes:
                attributes[attr_type] = []

            attributes[attr_type].append({"name": attr_name, "val": attr_value})

        return attributes
