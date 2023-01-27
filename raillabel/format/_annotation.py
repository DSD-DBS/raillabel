# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .coordinate_system import CoordinateSystem


@dataclass
class _Annotation(ABC):

    uid: str
    name: str
    attributes: t.Dict[str, t.Union[int, float, bool, str, list]] = field(default_factory=dict)
    coordinate_system: CoordinateSystem = None
    object_annotations: t.Any = None

    @property
    def uri(self) -> str or None:
        """URI to the file, which contains the annotated object."""
        if self.object_annotations is None or self.object_annotations.frame is None:
            return None
        return self.object_annotations.frame.streams[self.coordinate_system.uid].uri

    @uri.setter
    def uri(self, value):

        if self.object_annotations is None:
            raise AttributeError(f"Attribute object_annotations not set for annotation {self.uri}.")

        if self.object_annotations.frame is None:
            raise AttributeError(
                f"Attribute frame not set for ObjectAnnotation of annotation {self.uri}."
            )

        self.object_annotations.frame.streams[self.coordinate_system.uid].uri = value

        return

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
    def fromdict(self, data_dict: t.Dict, coordinate_systems: t.Dict) -> t.Tuple[t.Dict, list]:
        """Generate a Bbox object from a dictionary in the OpenLABEL format.

        Parameters
        ----------
        data_dict: dict
            OpenLABEL format dictionary containing the data for the annotation.
        coordinate_systems: dict
            Dictionary containing all coordinate_systems for the scene.

        Returns
        -------
        annotation: Bbox
            Converted annotation.
        warnings: list of str
            List of non-critical errors, that have occurred during the conversion.
        """
        raise NotImplementedError

    @classmethod
    def equals(self, child: object, other: object):
        """Compare a child of annotation with another object.

        Parameters
        ----------
        child: t.Any
            Child of this class.
        other: t.Any
            Object to compare the child to.

        Returns
        -------
        bool
            True, if the child is equal to the other.
        """

        if type(child) != type(other):
            return False

        # object_annotations is omitted from the equal comparison, because it contains this
        # annotation, which will lead to a RecursionError.
        return {k: v for k, v in vars(child).items() if k != "object_annotations"} == {
            k: v for k, v in vars(other).items() if k != "object_annotations"
        }

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

        if self.coordinate_system is not None:
            dict_repr["coordinate_system"] = str(self.coordinate_system.uid)

        if self.attributes != {} or self.uri is not None:
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

                elif type(attr_value) in [list, t.Tuple]:
                    attr_type = "vec"

                else:
                    raise TypeError(
                        f"Attribute type {attr_value.__class__.__name__} of {attr_value} is not "
                        + "supported. Supported types are str, float, int, bool, list, t.Tuple."
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
