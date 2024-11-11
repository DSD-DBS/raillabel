# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from raillabel.json_format import JSONCuboid

from ._attributes import _attributes_from_json
from .point3d import Point3d
from .quaternion import Quaternion
from .size3d import Size3d


@dataclass
class Cuboid:
    """3D bounding box.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier of the annotation.
    pos: raillabel.format.Point3d
        The center position of the cuboid in meters, where the x coordinate points ahead of the
        vehicle, y points to the left and z points upwards.
    quat: raillabel.format.Quaternion
        The rotation of the cuboid in quaternions.
    size: raillabel.format.Size3d
        The size of the cuboid in meters.
    object: raillabel.format.Object
        A reference to the object, this annotation belongs to.
    sensor: raillabel.format.Sensor
        A reference to the sensor, this annotation is labeled in. Default is None.
    attributes: dict, optional
        Attributes of the annotation. Dict keys are the name str of the attribute, values are the
        attribute values. Default is {}.

    Properties (read-only)
    ----------------------
    name: str
        Name of the annotation used by the VCD player for indexing in the object data pointers.

    """

    pos: Point3d
    """The center position of the cuboid in meters, where the x coordinate points ahead of the
    vehicle, y points to the left and z points upwards."""

    quat: Quaternion
    "The rotation of the cuboid in quaternions."

    size: Size3d
    "The size of the cuboid in meters."

    object: UUID
    "The uid of the object, this annotation belongs to."

    sensor: str
    "The uid of the sensor, this annotation is labeled in."

    attributes: dict[str, float | bool | str | list]
    "Additional information associated with the bbox."

    @classmethod
    def from_json(cls, json: JSONCuboid, object_uid: UUID) -> Cuboid:
        """Construct an instant of this class from RailLabel JSON data."""
        return Cuboid(
            pos=Point3d.from_json((json.val[0], json.val[1], json.val[2])),
            quat=Quaternion.from_json((json.val[3], json.val[4], json.val[5], json.val[6])),
            size=Size3d.from_json((json.val[7], json.val[8], json.val[9])),
            object=object_uid,
            sensor=json.coordinate_system,
            attributes=_attributes_from_json(json.attributes),
        )
