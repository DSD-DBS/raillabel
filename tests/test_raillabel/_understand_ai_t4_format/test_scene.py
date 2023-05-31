# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

from test_frame import _prepare_frame_data

import raillabel._understand_ai_t4_format as uai_format


def remove_generated_fields(raillabel_data: dict) -> dict:
    """Return RailLabel file with object_data_pointers and frame_intervals
    removed."""

    raillabel_data = _remove_frame_intervals(raillabel_data)
    raillabel_data = _remove_object_data_pointers(raillabel_data)
    raillabel_data = _remove_annotation_names(raillabel_data)

    return raillabel_data

def _remove_frame_intervals(raillabel_data: dict) -> dict:
    if "frame_intervals" in raillabel_data["openlabel"]:
        del raillabel_data["openlabel"]["frame_intervals"]

    for object in raillabel_data["openlabel"]["objects"]:
        if "frame_intervals" in raillabel_data["openlabel"]["objects"][object]:
            del raillabel_data["openlabel"]["objects"][object]["frame_intervals"]

    return raillabel_data

def _remove_object_data_pointers(raillabel_data: dict) -> dict:
    for object in raillabel_data["openlabel"]["objects"]:
        if "object_data_pointers" in raillabel_data["openlabel"]["objects"][object]:
            del raillabel_data["openlabel"]["objects"][object]["object_data_pointers"]

    return raillabel_data

def _remove_annotation_names(raillabel_data: dict) -> dict:
    for frame in raillabel_data["openlabel"]["frames"].values():
        for object in frame["objects"].values():
            for annotations in object["object_data"].values():
                for annotation in annotations:
                    if "name" in annotation:
                        annotation["name"] = annotation["uid"]
                        del annotation["uid"]

    return raillabel_data


def remove_non_parsed_fields(raillabel_data: dict) -> dict:
    """Return RailLabel file with frame_data and poly3ds removed."""

    for frame in raillabel_data["openlabel"]["frames"].values():

        if "frame_data" in frame["frame_properties"]:
            del frame["frame_properties"]["frame_data"]

        for object_id, object in list(frame["objects"].items()):
            if "poly3d" not in object["object_data"]:
                continue

            del object["object_data"]["poly3d"]
            if len(object["object_data"]) == 0:
                del frame["objects"][object_id]

    return raillabel_data


def test_fromdict(json_data):
    input_data = {
        "metadata": json_data["_understand_ai_t4_format/metadata"],
        "coordinateSystems": [
            json_data["_understand_ai_t4_format/coordinate_system_camera"],
            json_data["_understand_ai_t4_format/coordinate_system_lidar"],
        ],
        "frames": [
            _prepare_frame_data(json_data["_understand_ai_t4_format/frame"], json_data),
        ]
    }
    scene = uai_format.Scene.fromdict(input_data)

    assert scene.metadata == uai_format.Metadata.fromdict(input_data["metadata"])
    assert len(scene.coordinate_systems) == 2
    assert scene.coordinate_systems[input_data["coordinateSystems"][0]["coordinate_system_id"]] == uai_format.CoordinateSystem.fromdict(input_data["coordinateSystems"][0])
    assert scene.coordinate_systems[input_data["coordinateSystems"][1]["coordinate_system_id"]] == uai_format.CoordinateSystem.fromdict(input_data["coordinateSystems"][1])
    assert len(scene.frames) == 1
    assert scene.frames[input_data["frames"][0]["frameId"]] == uai_format.Frame.fromdict(input_data["frames"][0])


def test_to_raillabel(json_data):
    input_data = json_data["understand_ai_t4_short"]
    input_data["metadata"] = json_data["_understand_ai_t4_format/metadata"]
    scene = uai_format.Scene.fromdict(json_data["understand_ai_t4_short"])
    output_data = scene.to_raillabel()

    ground_truth = remove_generated_fields(json_data["openlabel_v1_short"])
    ground_truth = remove_non_parsed_fields(ground_truth)

    ground_truth["openlabel"]["metadata"] = None
    output_data["openlabel"]["metadata"] = None

    assert output_data == ground_truth


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
