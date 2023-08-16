# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field

from .._util._attribute_type import AttributeType
from .._util._warning import _warning
from .sensor import Sensor


@dataclass
class _Annotation(ABC):

    uid: str
    name: str
    attributes: t.Dict[str, t.Union[int, float, bool, str, list]] = field(default_factory=dict)
    sensor: Sensor = None

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
    def fromdict(cls, data_dict: t.Dict, sensors: t.Dict) -> t.Type["_Annotation"]:
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
            dict_repr["attributes"] = {}

            for attr_name, attr_value in self.attributes.items():

                attr_type = AttributeType.from_value(type(attr_value)).value

                if attr_type not in dict_repr["attributes"]:
                    dict_repr["attributes"][attr_type] = []

                dict_repr["attributes"][attr_type].append({"name": attr_name, "val": attr_value})

        return dict_repr

    @classmethod
    def _coordinate_system_fromdict(cls, data_dict: dict, sensors: dict) -> t.Optional[Sensor]:

        is_coordinate_system_in_data = (
            "coordinate_system" in data_dict and data_dict["coordinate_system"] != ""
        )

        if not is_coordinate_system_in_data:
            return None

        if data_dict["coordinate_system"] not in sensors:
            _warning(
                f"{data_dict['coordinate_system']} does not exist as a coordinate system, "
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
