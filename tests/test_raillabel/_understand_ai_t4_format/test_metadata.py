# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel._understand_ai_t4_format as uai_format


def test_fromdict(json_data):
    input_data = json_data["_understand_ai_t4_format/metadata"]
    metadata = uai_format.Metadata.fromdict(input_data)

    assert metadata.clip_id == input_data["clip_id"]
    assert metadata.external_clip_id == input_data["external_clip_id"]
    assert metadata.project_id == input_data["project_id"]
    assert metadata.export_time == input_data["export_time"]
    assert metadata.exporter_version == input_data["exporter_version"]
    assert metadata.coordinate_system_3d == input_data["coordinate_system_3d"]
    assert metadata.coordinate_system_reference == input_data["coordinate_system_reference"]
    assert metadata.folder_name == input_data["folder_name"]

def test_to_raillabel(json_data):
    input_data = json_data["_understand_ai_t4_format/metadata"]
    output_data = uai_format.Metadata.fromdict(input_data).to_raillabel()
    ground_truth = json_data["_understand_ai_t4_format/metadata_raillabel"]
    ground_truth["subschema_version"] = json_data["raillabel_v2_schema"]["version"]

    assert output_data == ground_truth

# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
