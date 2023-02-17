# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field

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

    # === Public Methods =====================================================

    @abstractmethod
    def asdict(self) -> t.Dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this class instance.

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def fromdict(self, data_dict: t.Dict, sensors: t.Dict) -> t.Tuple[t.Dict, list]:
        """Generate a Bbox object from a dictionary in the OpenLABEL format.

        Parameters
        ----------
        data_dict: dict
            OpenLABEL format dictionary containing the data for the annotation.
        sensors: dict
            Dictionary containing all sensors for the scene.

        Returns
        -------
        annotation: Bbox
            Converted annotation.
        warnings: list of str
            List of non-critical errors, that have occurred during the conversion.
        """
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

                # Since the annotation stores the attributes in a collective
                # dictionary, they must be seperated by type in order to comply
                # with the OpenLabel format.

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

                if attr_type not in dict_repr["attributes"]:
                    dict_repr["attributes"][attr_type] = []

                dict_repr["attributes"][attr_type].append({"name": attr_name, "val": attr_value})

        return dict_repr

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
