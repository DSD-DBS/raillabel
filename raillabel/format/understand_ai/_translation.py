# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
from pathlib import Path


def translate_sensor_id(original_sensor_id: str) -> str:
    """Translate deprecated sensor ids to the correct ones.

    Parameters
    ----------
    original_sensor_id : str
        Original id of the sensor.

    Returns
    -------
    str
        Translated id or original_sensor_id, if no translation could be found.
    """
    return TRANSLATION["streams"].get(original_sensor_id, original_sensor_id)


def translate_class_id(original_class_id: str) -> str:
    """Translate deprecated class ids to the correct ones.

    Parameters
    ----------
    original_class_id : str
        Original id of the class.

    Returns
    -------
    str
        Translated id or original_class_id, if no translation could be found.
    """
    return TRANSLATION["classes"].get(original_class_id, original_class_id)


def fetch_sensor_type(sensor_id: str) -> str:
    """Fetch sensor type from translation file.

    Parameters
    ----------
    sensor_id : str
        Id of the sensor.

    Returns
    -------
    str
        Sensor type or 'other' if sensor_id not found in translation.json.
    """
    return TRANSLATION["stream_types"].get(sensor_id, "other")


def fetch_sensor_resolutions(sensor_id: str) -> dict:
    """Fetch sensor resolution from translation file.

    Parameters
    ----------
    sensor_id : str
        Id of the sensor.

    Returns
    -------
    dict
        Dictionary containing the resolution information. Key 'x' contains the width in pixels,
        key 'y' contains the height in pixels. If the sensor is a radar, 'resolution_px_per_m' is
        also included.
    """
    return TRANSLATION["stream_resolutions"].get(
        sensor_id, {"x": None, "y": None, "resolution_px_per_m": None}
    )


def _load_translation():
    """Load the translation file when the module is imported.

    This prevents it from beeing loaded for every annotation.
    """

    global TRANSLATION

    translatiion_path = (
        Path(__file__).parent.parent.parent / "load_" / "loader_classes" / "translation.json"
    )
    with translatiion_path.open() as translation_file:
        TRANSLATION = json.load(translation_file)


TRANSLATION = {}

_load_translation()
