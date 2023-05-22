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


def _load_translation():
    """Load the translation file when the module is imported.

    This prevents it from beeing loaded for every annotation.
    """

    global TRANSLATION

    translatiion_path = Path(__file__).parent.parent / "format_loaders" / "translation.json"
    with translatiion_path.open() as translation_file:
        TRANSLATION = json.load(translation_file)


_load_translation()
