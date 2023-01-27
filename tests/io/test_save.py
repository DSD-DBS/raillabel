# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

import raillabel


def test_save(openlabel_v1_short_data):
    with tempfile.TemporaryDirectory("w") as temp_dir:

        # Removes the object data pointers from the example file so that it needs to be generated from the data
        for object in openlabel_v1_short_data["openlabel"]["objects"].values():
            del object["frame_intervals"]
            del object["object_data_pointers"]

        with (Path(temp_dir) / "stripped_input_data.json").open("w") as f:
            json.dump(openlabel_v1_short_data, f)

        scene_orig = raillabel.load(Path(temp_dir) / "stripped_input_data.json", False, False)

        raillabel.save(scene_orig, Path(temp_dir) / "test_save_file.json")
        scene_saved = raillabel.load(Path(temp_dir) / "test_save_file.json", False, False)

    assert scene_orig == scene_saved


# Executes the test if the file is called
if __name__ == "__main__":
    pytest.main([__file__, "--disable-pytest-warnings"])
