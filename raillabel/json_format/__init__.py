# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Package for classes representing the direct RailLabel JSON objects."""

from .attributes import JSONAttributes
from .bbox import JSONBbox
from .boolean_attribute import JSONBooleanAttribute
from .coordinate_system import JSONCoordinateSystem
from .cuboid import JSONCuboid
from .element_data_pointer import JSONElementDataPointer
from .frame import JSONFrame, JSONFrameData, JSONFrameProperties
from .frame_interval import JSONFrameInterval
from .metadata import JSONMetadata
from .num import JSONNum
from .num_attribute import JSONNumAttribute
from .object import JSONObject
from .object_data import JSONAnnotations, JSONObjectData
from .poly2d import JSONPoly2d
from .poly3d import JSONPoly3d
from .scene import JSONScene, JSONSceneContent
from .stream_camera import JSONIntrinsicsPinhole, JSONStreamCamera, JSONStreamCameraProperties
from .stream_other import JSONStreamOther
from .stream_radar import JSONIntrinsicsRadar, JSONStreamRadar, JSONStreamRadarProperties
from .stream_sync import JSONStreamSync, JSONStreamSyncProperties, JSONStreamSyncTimestamp
from .text_attribute import JSONTextAttribute
from .transform_data import JSONTransformData
from .vec import JSONVec
from .vec_attribute import JSONVecAttribute

__all__ = [
    "JSONAnnotations",
    "JSONAttributes",
    "JSONBbox",
    "JSONBooleanAttribute",
    "JSONCoordinateSystem",
    "JSONCuboid",
    "JSONElementDataPointer",
    "JSONFrameInterval",
    "JSONFrame",
    "JSONFrameData",
    "JSONFrameProperties",
    "JSONMetadata",
    "JSONNumAttribute",
    "JSONNum",
    "JSONObjectData",
    "JSONObject",
    "JSONPoly2d",
    "JSONPoly3d",
    "JSONScene",
    "JSONSceneContent",
    "JSONStreamCamera",
    "JSONStreamCameraProperties",
    "JSONIntrinsicsPinhole",
    "JSONStreamOther",
    "JSONStreamRadar",
    "JSONStreamRadarProperties",
    "JSONIntrinsicsRadar",
    "JSONStreamSync",
    "JSONStreamSyncProperties",
    "JSONStreamSyncTimestamp",
    "JSONTextAttribute",
    "JSONTransformData",
    "JSONVecAttribute",
    "JSONVec",
]
