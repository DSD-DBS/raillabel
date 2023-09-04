# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules

from ..._util._attribute_type import AttributeType
from ..._util._warning import _warning
from .object import Object
from .sensor import Sensor


@dataclass
class _ObjectAnnotation(ABC):

    uid: str
    object: Object
    sensor: t.Optional[Sensor] = None
    attributes: t.Dict[str, t.Union[int, float, bool, str, list]] = field(default_factory=dict)

    @property
    def name(self) -> str:
        if self.sensor is None:
            raise AttributeError(
                f"Annotation {self.uid} does not have a 'sensor', which is required "
                + "to create the name."
            )

        return f"{self.sensor.uid}__{self.OPENLABEL_ID}__{self.object.type}"

    @property
    @abstractproperty
    def _REQ_FIELDS(self) -> t.List[str]:
        raise NotImplementedError

    @property
    @abstractproperty
    def OPENLABEL_ID(self) -> t.List[str]:
        raise NotImplementedError

    # === Public Methods =====================================================

    @abstractmethod
    def asdict(self) -> t.Dict:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def fromdict(
        cls,
        data_dict: t.Dict,
        sensors: t.Dict,
        object: Object,
    ) -> t.Type["_ObjectAnnotation"]:
        raise NotImplementedError

    # === Private Methods ====================================================

    def _annotation_required_fields_asdict(self) -> t.Dict:
        """Return the required fields from the parent class to dict."""
        return {
            "uid": str(self.uid),
            "name": str(self.name),
        }

    def _annotation_optional_fields_asdict(self) -> t.Dict:
        """Return the optional fields from the parent class to dict."""

        dict_repr = {}

        if self.sensor is not None:
            dict_repr["coordinate_system"] = str(self.sensor.uid)

        if self.attributes != {}:
            dict_repr["attributes"] = self._attributes_asdict(self.attributes)

        return dict_repr

    def _attributes_asdict(self, attributes: dict) -> dict:
        attributes_dict = {}

        for attr_name, attr_value in attributes.items():

            attr_type = AttributeType.from_value(type(attr_value)).value

            if attr_type not in attributes_dict:
                attributes_dict[attr_type] = []

            attributes_dict[attr_type].append({"name": attr_name, "val": attr_value})

        return attributes_dict

    @classmethod
    def _coordinate_system_fromdict(cls, data_dict: dict, sensors: dict) -> t.Optional[Sensor]:

        is_coordinate_system_in_data = (
            "coordinate_system" in data_dict and data_dict["coordinate_system"] != ""
        )

        if not is_coordinate_system_in_data:
            return None

        if data_dict["coordinate_system"] not in sensors:
            _warning(
                f"'{data_dict['coordinate_system']}' does not exist as a sensor, "
                + f"but is referenced for the annotation {data_dict['uid']}."
            )
            return None

        return sensors[data_dict["coordinate_system"]]

    @classmethod
    def _attributes_fromdict(
        cls,
        data_dict: dict,
    ) -> t.Dict[str, t.Union[int, float, bool, str, list]]:

        if "attributes" not in data_dict:
            return {}

        return {a["name"]: a["val"] for l in data_dict["attributes"].values() for a in l}

    # === Special Methods ====================================================

    def __post_init__(self):
        """Check for required arguments after __init__.

        Inheritance in dataclasses has the flaw, that when the parent class has fields with
        defaults and the child class has fields without, a TypeError is raised due to required
        fields following optional ones. This is solved by making all fields in the child
        optional and checking for required fields in __post_init__().

        Raises
        ------
        TypeError
            If a required field has not been set.
        """

        for f in self._REQ_FIELDS:
            if getattr(self, f) is None:
                raise TypeError(f"{f} is a required argument for {self.__class__.__name__}")


def annotation_classes() -> t.Dict[str, t.Type[_ObjectAnnotation]]:
    """Return dictionary with _Annotation child classes."""
    return ANNOTATION_CLASSES


def _collect_annotation_classes():
    """Collect annotation child classes and store them."""

    global ANNOTATION_CLASSES

    package_dir = str(Path(__file__).resolve().parent)
    for (_, module_name, _) in iter_modules([package_dir]):

        module = import_module(f"raillabel.format.raillabel.{module_name}")
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if (
                isclass(attribute)
                and issubclass(attribute, _ObjectAnnotation)
                and attribute != _ObjectAnnotation
            ):
                ANNOTATION_CLASSES[attribute.OPENLABEL_ID] = attribute


ANNOTATION_CLASSES = {}
_collect_annotation_classes()
