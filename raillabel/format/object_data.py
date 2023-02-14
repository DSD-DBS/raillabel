# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from dataclasses import dataclass, field

from ._annotation import _Annotation
from .bbox import Bbox
from .cuboid import Cuboid
from .object import Object
from .poly2d import Poly2d
from .poly3d import Poly3d
from .seg3d import Seg3d


@dataclass
class ObjectData:
    """Annotations associated with a specific object in a frame.

    Parameters
    ----------
    object: raillabel.format.Object
        A reference to the object this ObjectData belongs to.
    annotations: dict, optional
        Dictionary of all annotations representing this object in this frame.

    Properties (read-only)
    ----------------------
    bboxs: dict of raillabel.format.Bbox
        Dictionary of all bounding boxes representing this object in this frame.
    cuboids: dict of raillabel.format.Cuboid
        Dictionary of all cuboids representing this object in this frame.
    poly2ds: dict of raillabel.format.Poly2d
        Dictionary of all 2d polylines representing this object in this frame.
    poly3ds: dict of raillabel.format.Poly3d
        Dictionary of all 3d polylines representing this object in this frame.
    seg3ds: dict of raillabel.format.Seg3d
        Dictionary of all 3d segmentations representing this object in this frame.
    """

    object: Object
    annotations: t.Dict[str, t.Type[_Annotation]] = field(default_factory=dict)

    @property
    def bboxs(self) -> t.Dict[str, Bbox]:
        """Return dictionary of all bounding boxes."""
        return {k: v for k, v in self.annotations.items() if isinstance(v, Bbox)}

    @property
    def cuboids(self) -> t.Dict[str, Cuboid]:
        """Return dictionary of all cuboids."""
        return {k: v for k, v in self.annotations.items() if isinstance(v, Cuboid)}

    @property
    def poly2ds(self) -> t.Dict[str, Poly2d]:
        """Return dictionary of all 2d poly lines."""
        return {k: v for k, v in self.annotations.items() if isinstance(v, Poly2d)}

    @property
    def poly3ds(self) -> t.Dict[str, Bbox]:
        """Return dictionary of all 3d poly lines."""
        return {k: v for k, v in self.annotations.items() if isinstance(v, Poly3d)}

    @property
    def seg3ds(self) -> t.Dict[str, Seg3d]:
        """Return dictionary of all 3d segmentations."""
        return {k: v for k, v in self.annotations.items() if isinstance(v, Seg3d)}

    def asdict(self) -> dict:
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

        dict_repr = {"object_data": {}}

        if self.bboxs != {}:
            dict_repr["object_data"]["bbox"] = []

            for bbox in self.bboxs.values():
                dict_repr["object_data"]["bbox"].append(bbox.asdict())

        if self.poly2ds != {}:
            dict_repr["object_data"]["poly2d"] = []

            for poly2d in self.poly2ds.values():
                dict_repr["object_data"]["poly2d"].append(poly2d.asdict())

        if self.poly3ds != {}:
            dict_repr["object_data"]["poly3d"] = []

            for poly3d in self.poly3ds.values():
                dict_repr["object_data"]["poly3d"].append(poly3d.asdict())

        if self.cuboids != {}:
            dict_repr["object_data"]["cuboid"] = []

            for cuboid in self.cuboids.values():
                dict_repr["object_data"]["cuboid"].append(cuboid.asdict())

        if self.seg3ds != {}:
            dict_repr["object_data"]["vec"] = []

            for seg3d in self.seg3ds.values():
                dict_repr["object_data"]["vec"].append(seg3d.asdict())

        return dict_repr


class AnnotationContainer(dict):
    """Advanced version of a dictionary.

    When an element is referenced, it is first searched by its key and
    then by the elements name property. Enables searching by the
    annotation uid and the annotation name.
    """

    @property
    def switched_keys(self):
        """Return the dictionary with the keys switched out to the names."""
        return {v.name: v for v in super().values()}

    def __getitem__(self, __key: str) -> object:
        """Return the item either from the uid or the name."""
        try:
            return super().__getitem__(__key)
        except KeyError as e:
            try:
                return self.switched_keys[__key]
            except KeyError as e1:
                raise e from e1

    def __contains__(self, __o: object) -> bool:
        """Return true if the object is in the dict."""
        if super().__contains__(__o):
            return True
        return self.switched_keys.__contains__(__o)
