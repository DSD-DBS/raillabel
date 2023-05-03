# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(1, str(Path(__file__).parent.parent.parent.parent))

import raillabel
import raillabel._understand_ai_t4_format as uai_format


def test_fromdict():
    metadata = uai_format.Metadata.fromdict({
        "clip_id": "db_3_2021-09-22-14-28-01_2021-09-22-14-44-03",
        "external_clip_id": "2021-09-22-14-28-01_2021-09-22-14-44-03",
        "project_id": "trains_4",
        "export_time": "2023-04-20 01:38 UTC",
        "exporter_version": "1.0.0",
        "coordinate_system_3d": "FLU",
        "coordinate_system_reference": "SENSOR",
        "folder_name": "2021-09-22-14-28-01_2021-09-22-14-44-03"
    })

    assert metadata.clip_id == "db_3_2021-09-22-14-28-01_2021-09-22-14-44-03"
    assert metadata.external_clip_id == "2021-09-22-14-28-01_2021-09-22-14-44-03"
    assert metadata.project_id == "trains_4"
    assert metadata.export_time == "2023-04-20 01:38 UTC"
    assert metadata.exporter_version == "1.0.0"
    assert metadata.coordinate_system_3d == "FLU"
    assert metadata.coordinate_system_reference == "SENSOR"
    assert metadata.folder_name == "2021-09-22-14-28-01_2021-09-22-14-44-03"


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
