# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from abc import ABC, abstractproperty
from dataclasses import dataclass
from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules
from typing import Any

from ._attribute_type import AttributeType
from .object import Object
from .sensor import Sensor


@dataclass
class _ObjectAnnotation(ABC):
    uid: str
    object: Object
    sensor: Sensor
    attributes: dict[str, int | float | bool | str | list]

    @property
    def name(self) -> str:
        return f"{self.sensor.uid}__{self.OPENLABEL_ID}__{self.object.type}"

    @property
    @abstractproperty
    def OPENLABEL_ID(self) -> list[str] | str:
        raise NotImplementedError

    # === Private Methods ====================================================

    def _annotation_required_fields_asdict(self) -> dict:
        """Return the required fields from the parent class to dict."""
        return {
            "uid": str(self.uid),
            "name": str(self.name),
        }

    def _annotation_optional_fields_asdict(self) -> dict[str, Any]:
        """Return the optional fields from the parent class to dict."""
        dict_repr: dict[str, Any] = {}

        if self.sensor is not None:
            dict_repr["coordinate_system"] = str(self.sensor.uid)

        if self.attributes != {}:
            dict_repr["attributes"] = self._attributes_asdict(self.attributes)

        return dict_repr

    def _attributes_asdict(self, attributes: dict[str, Any]) -> dict[str, Any]:
        attributes_dict: dict[str, Any] = {}

        for attr_name, attr_value in attributes.items():
            attr_type = AttributeType.from_value(type(attr_value)).value

            if attr_type not in attributes_dict:
                attributes_dict[attr_type] = []

            attributes_dict[attr_type].append({"name": attr_name, "val": attr_value})

        return attributes_dict

    @classmethod
    def _coordinate_system_fromdict(cls, data_dict: dict, sensors: dict) -> Sensor:
        return sensors[data_dict["coordinate_system"]]

    @classmethod
    def _attributes_fromdict(
        cls,
        data_dict: dict,
    ) -> dict[str, int | float | bool | str | list]:
        if "attributes" not in data_dict:
            return {}

        return {a["name"]: a["val"] for type_ in data_dict["attributes"].values() for a in type_}


def annotation_classes() -> dict[str, type[_ObjectAnnotation]]:
    """Return dictionary with _Annotation child classes."""
    out = {}

    package_dir = str(Path(__file__).resolve().parent)
    for _, module_name, _ in iter_modules([package_dir]):
        module = import_module(f"raillabel.format.{module_name}")
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if (
                isclass(attribute)
                and issubclass(attribute, _ObjectAnnotation)
                and attribute != _ObjectAnnotation
            ):
                out[attribute.OPENLABEL_ID] = attribute

    return out  # type: ignore
