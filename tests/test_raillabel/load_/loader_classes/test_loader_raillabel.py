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
    return raillabel.load_.loader_classes.LoaderRailLabel()


def test_supports_true(json_data, loader):
    assert loader.supports(json_data["openlabel_v1_short"])


def test_supports_false(json_data, loader):
    data = json_data["openlabel_v1_short"]
    data["openlabel"]["metadata"]["subschema_version"] = "4.0.0"
    assert not loader.supports(data)


# Tests the warnings and errors
def test_no_warnings(json_data, loader):
    loader.load(json_data["openlabel_v1_short"], validate=False)
    assert len(loader.warnings) == 0


def test_warnings_sync(json_data, loader):
    data = json_data["openlabel_v1_short"]

    data["openlabel"]["frames"]["0"]["frame_properties"]["streams"]["non_existing_stream"] = {
        "stream_properties": {
            "sync": {
                "timestamp": "1632321743.100000072"
            }
        }
    }

    loader.load(data, validate=False)
    assert len(loader.warnings) == 1

    # Tests for keywords in the warning that can help the user identify the source
    assert "frame" in loader.warnings[0]
    assert "0" in loader.warnings[0]
    assert "sync" in loader.warnings[0]
    assert "non_existing_stream" in loader.warnings[0]


def test_warnings_stream_sync_field(json_data, loader):
    data = json_data["openlabel_v1_short"]

    data["openlabel"]["frames"]["0"]["frame_properties"]["streams"][
        "rgb_middle"
    ]["stream_properties"]["stream_sync"] = data["openlabel"]["frames"]["0"][
        "frame_properties"
    ][
        "streams"
    ][
        "rgb_middle"
    ][
        "stream_properties"
    ][
        "sync"
    ]
    del data["openlabel"]["frames"]["0"]["frame_properties"]["streams"][
        "rgb_middle"
    ]["stream_properties"]["sync"]

    loader.load(data, validate=False)
    assert len(loader.warnings) == 1

    # Tests for keywords in the warning that can help the user identify the source
    assert "stream_sync" in loader.warnings[0]
    assert "deprecated" in loader.warnings[0].lower()
    assert "save()" in loader.warnings[0]


def test_identify_of_references(json_data, loader):
    data = json_data["openlabel_v1_short"]

    scene = loader.load(data, validate=False)

    for frame in scene.frames.values():

        for sensor_reference in frame.sensors.values():
            assert sensor_reference.sensor is scene.sensors[sensor_reference.sensor.uid]

        for frame_data in frame.frame_data.values():
            assert frame_data.sensor is scene.sensors[frame_data.sensor.uid]

        for annotation in frame.annotations.values():
            assert annotation.sensor is scene.sensors[annotation.sensor.uid]


# Executes the test if the file is called
if __name__ == "__main__":
    os.system("clear")
    pytest.main([__file__, "--disable-pytest-warnings", "--cache-clear"])
