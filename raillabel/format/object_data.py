# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
import uuid
from dataclasses import dataclass, field

from .._util._warning import _warning
from ._annotation import _Annotation
from .bbox import Bbox
from .cuboid import Cuboid
from .object import Object
from .poly2d import Poly2d
from .poly3d import Poly3d
from .seg3d import Seg3d
from .sensor import Sensor


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

    @classmethod
    def fromdict(
        cls,
        uid: str,
        data_dict: dict,
        objects: t.Dict[str, Object],
        sensors: t.Dict[str, Sensor],
        annotation_classes: dict,
    ) -> "ObjectData":
        """Generate a ObjectData object from a dict.

        Parameters
        ----------
        uid: str
            Unique identifier of the object.
        data_dict: dict
            RailLabel format snippet containing the relevant data.
        objects: dict
            Dictionary of all objects in the scene.
        sensors: dict
            Dictionary of all sensors in the scene.
        annotation_classes: dict
            Dictionary conaining all of the annotation classes as values
            with the OpenLABEL identifiers as keys.

        Returns
        -------
        object_data: raillabel.format.ObjectData
            Converted ObjectData object.
        """

        object_data = ObjectData(object=objects[uid])

        for ann_type in data_dict:

            if ann_type not in annotation_classes:
                _warning(
                    f"Annotation type {ann_type} is currently not supported. Supported "
                    + "annotation types: "
                    + str(list(annotation_classes.keys()))
                )
                continue

            for ann_raw in data_dict[ann_type]:

                ann_raw = cls._fix_deprecated_annotation_name(ann_raw, ann_type, objects[uid].type)

                if ann_raw["uid"] in object_data.annotations:
                    _warning(
                        f"Annotation '{ann_raw['uid']}' is contained more than one "
                        + "time. A new UID is beeing assigned."
                    )
                    ann_raw["uid"] = str(uuid.uuid4())

                object_data.annotations[ann_raw["uid"]] = annotation_classes[ann_type].fromdict(
                    ann_raw,
                    sensors,
                )

        return object_data

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

    @classmethod
    def _fix_deprecated_annotation_name(cls, ann_raw: dict, ann_type: str, obj_type: str) -> dict:

        if "uid" not in ann_raw:
            try:
                ann_raw["uid"] = str(uuid.UUID(ann_raw["name"]))
            except ValueError:
                ann_raw["uid"] = str(uuid.uuid4())

        ann_raw["name"] = f"{ann_raw['coordinate_system']}__{ann_type}__{obj_type}"

        return ann_raw
