# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel


@pytest.fixture
def loader():
    return raillabel.format_loaders.LoaderUnderstandAiT4()


def test_supports_true(json_data, loader):
    assert loader.supports(json_data["understand_ai_real_life"])


def test_supports_false(json_data, loader):
    data = json_data["understand_ai_real_life"]
    del data["metadata"]["project_id"]
    assert not loader.supports(data)


def test_load(json_data, loader):
    input_data_raillabel = remove_non_parsed_fields(json_data["openlabel_v1_short"])
    input_data_uai = json_data["understand_ai_t4_short"]

    scene_ground_truth = raillabel.format_loaders.LoaderRailLabelV2().load(input_data_raillabel, validate=False)
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


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
