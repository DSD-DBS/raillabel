# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
import os
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

import raillabel


def test_save_scene(openlabel_v1_short_path):
    with tempfile.TemporaryDirectory("w") as temp_dir:

        scene_orig = raillabel.load(openlabel_v1_short_path, False, False)

        raillabel.save(scene_orig, Path(temp_dir) / "test_save_file.json")
        scene_saved = raillabel.load(Path(temp_dir) / "test_save_file.json", False, False)

    assert scene_orig == scene_saved


def test_save_json(openlabel_v1_short_data):
    with tempfile.TemporaryDirectory("w") as temp_dir:

        stripped_input_data = deepcopy(openlabel_v1_short_data)

        # Removes the object data pointers from the example file so that it needs to be generated from the data
        for object in stripped_input_data["openlabel"]["objects"].values():
            del object["frame_intervals"]
            del object["object_data_pointers"]

        with (Path(temp_dir) / "stripped_input_data.json").open("w") as f:
            json.dump(stripped_input_data, f)

        scene = raillabel.load(Path(temp_dir) / "stripped_input_data.json", False, False)
        raillabel.save(scene, Path(temp_dir) / "test_save_file.json")

        with (Path(temp_dir) / "test_save_file.json").open() as f:
            saved_and_loaded_data = json.load(f)

    # Removes the exporter version from the generated file as these are hard to test for
    if "exporter_version" in saved_and_loaded_data["openlabel"]["metadata"]:
        del saved_and_loaded_data["openlabel"]["metadata"]["exporter_version"]

    assert saved_and_loaded_data == openlabel_v1_short_data


def test_frame_intervals():
    data = {
        "openlabel": {
            "metadata": {"schema_version": "1.0.0"},
            "frames": {
                "0": {},
                "1": {},
                "2": {},
                "5": {},
                "7": {},
                "8": {},
            },
        }
    }

    scene = raillabel.format_loaders.LoaderRailLabelV2().load(data)
    dict_repr = scene.asdict()["openlabel"]

    assert "frame_intervals" in dict_repr
    assert dict_repr["frame_intervals"] == [
        {"frame_start": 0, "frame_end": 2},
        {"frame_start": 5, "frame_end": 5},
        {"frame_start": 7, "frame_end": 8},
    ]


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
