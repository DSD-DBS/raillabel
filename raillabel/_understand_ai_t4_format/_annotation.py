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

    def to_raillabel(self) -> t.Tuple[dict, str, str, dict]:
        """Convert to a raillabel compatible dict.

        Returns
        -------
        bounding_box: dict
            Dictionary valid for the raillabel schema.
        object_id: str
            Friendly identifier of the object this sensor belongs to.
        class_name: str
            Friendly identifier of the class the annotated object belongs to.
        sensor_reference: dict
            Dictionary of the sensor reference.
        """

        return (
            {
                "name": str(self.id),
                "val": self._val_to_raillabel(),
                "coordinate_system": self.sensor.type,  # TODO: translate
                "attributes": self._attributes_to_raillabel(),
            },
            str(self.object_id),
            self.class_name,  # TODO: translate
            self.sensor.to_raillabel()[1],
        )

    def _attributes_to_raillabel(self) -> dict:

        attributes = {}

        for attr_name, attr_value in self.attributes.items():

            if type(attr_value) == str:
                attr_type = "text"

            elif type(attr_value) in [float, int]:
                attr_type = "num"

            elif type(attr_value) == bool:
                attr_type = "boolean"

            elif type(attr_value) in [list, tuple]:
                attr_type = "vec"

            else:
                raise TypeError(
                    f"Attribute type {attr_value.__class__.__name__} of {attr_value} is not "
                    + "supported. Supported types are str, float, int, bool, list, tuple."
                )

            if attr_type not in attributes:
                attributes[attr_type] = []

            attributes[attr_type].append({"name": attr_name, "val": attr_value})

        return attributes
