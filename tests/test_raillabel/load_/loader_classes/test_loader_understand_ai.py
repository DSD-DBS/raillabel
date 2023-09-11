# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent.parent))

import raillabel


@pytest.fixture
def loader():
    return raillabel.load_.loader_classes.LoaderUnderstandAi()


def test_supports_true(json_data, loader):
    assert loader.supports(json_data["understand_ai_real_life"])


def test_supports_false(json_data, loader):
    data = json_data["understand_ai_real_life"]
    del data["metadata"]["project_id"]
    assert not loader.supports(data)


def test_load(json_data, loader):
    input_data_raillabel = remove_non_parsed_fields(json_data["openlabel_v1_short"])
    input_data_uai = json_data["understand_ai_t4_short"]

    scene_ground_truth = raillabel.load_.loader_classes.LoaderRailLabel().load(input_data_raillabel, validate=False)
    scene = loader.load(input_data_uai, validate=False)

    scene.metadata = scene_ground_truth.metadata

    assert scene.asdict() == scene_ground_truth.asdict()

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


def test_raillabel_loader_warnings(loader):
    scene_dict = {
        "metadata": {
            "clip_id": "db_3_2021-09-22-14-28-01_2021-09-22-14-44-03",
            "external_clip_id": "2021-09-22-14-28-01_2021-09-22-14-44-03",
            "project_id": "trains_4",
            "export_time": "2023-04-20 01:38 UTC",
            "exporter_version": "1.0.0",
            "coordinate_system_3d": "FLU",
            "coordinate_system_reference": "SENSOR",
            "folder_name": "2021-09-22-14-28-01_2021-09-22-14-44-03"
        },
        "coordinateSystems": [],
        "frames": [
            {
                "frameId": "000",
                "timestamp": "1632321743.134149",
                "annotations": {
                    "2D_BOUNDING_BOX": [
                        {
                            "id": "78f0ad89-2750-4a30-9d66-44c9da73a714",
                            "objectId": "b40ba3ad-0327-46ff-9c28-2506cfd6d934",
                            "className": "2D_person",
                            "geometry": {
                                "xMin": -1.0,
                                "yMin": -0.5,
                                "xMax": 1,
                                "yMax": 2.5
                            },
                            "attributes": {},
                            "sensor": {
                                "type": "NON_EXISTENT_SENSOR",  # <-- relevant line
                                "uri": "S1206063/rgb_test0.png",
                                "timestamp": "1632321743.100000072"
                            }
                        }
                    ],
                    "2D_POLYLINE": [],
                    "2D_POLYGON": [],
                    "3D_BOUNDING_BOX": [],
                    "3D_SEGMENTATION": []
                }
            }
        ]
    }

    loader.load(scene_dict, validate=True)

    assert len(loader.warnings) == 2

    assert "NON_EXISTENT_SENSOR" in loader.warnings[0]
    assert "frame 0" in loader.warnings[0]

    assert "NON_EXISTENT_SENSOR" in loader.warnings[1]
    assert "78f0ad89-2750-4a30-9d66-44c9da73a714" in loader.warnings[1]

# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
