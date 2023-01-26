# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing
import uuid
from dataclasses import dataclass, field

from .bbox import Bbox
from .cuboid import Cuboid
from .object import Object
from .poly2d import Poly2d
from .seg3d import Seg3d


@dataclass
class ObjectAnnotations:
    """Annotations associated with a specific object in a frame.

    Parameters
    ----------
    object: raillabel.format.Object
        A reference to the object this ObjectData belongs to.
    bboxs: dict of raillabel.format.Bbox, optional
        Dictionary of all bounding boxes representing this object in this frame. Default is {}.
    cuboids: dict of raillabel.format.Cuboid, optional
        Dictionary of all cuboids representing this object in this frame. Default is {}.
    poly2ds: dict of raillabel.format.Poly2d, optional
        Dictionary of all polylines representing this object in this frame. Default is {}.
    seg3ds: dict of raillabel.format.Seg3d, optional
        Dictionary of all 3d segmentations representing this object in this frame. Default is {}.
    frame: raillabel.format.frame, optional
        Frame containing the ObjectAnnotations. Used for accessing higher level informations.
        Default is None.
    """

    object: Object
    bboxs: typing.Dict[uuid.UUID, Bbox] = field(default_factory=dict)
    cuboids: typing.Dict[uuid.UUID, Cuboid] = field(default_factory=dict)
    poly2ds: typing.Dict[uuid.UUID, Poly2d] = field(default_factory=dict)
    seg3ds: typing.Dict[uuid.UUID, Seg3d] = field(default_factory=dict)
    frame: typing.Any = None

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

        if self.cuboids != {}:
            dict_repr["object_data"]["cuboid"] = []

            for cuboid in self.cuboids.values():
                dict_repr["object_data"]["cuboid"].append(cuboid.asdict())

        if self.seg3ds != {}:
            dict_repr["object_data"]["vec"] = []

            for seg3d in self.seg3ds.values():
                dict_repr["object_data"]["vec"].append(seg3d.asdict())

        return dict_repr

    def __eq__(self, __o: object) -> bool:
        """Compare this object with another one."""

        if type(__o) != type(self):
            return False

        # frame is omitted from the equal comparison, because it contains this
        # annotation, which will lead to a RecursionError.
        return {k: v for k, v in vars(self).items() if k != "frame"} == {
            k: v for k, v in vars(__o).items() if k != "frame"
        }


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
