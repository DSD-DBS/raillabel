# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
import os
from pathlib import Path
from typing import List, Tuple

import jsonschema

from .. import exceptions


def validate(data: dict, schema_path: str = "openlabel_v1") -> Tuple[bool, List[str]]:
    """Validate JSON data represented by a dict via a given schema.

    Parameters
    ----------
    data: dict
        JSON data to be validated.
    schema_path: str, optional
        Path to the JSON schema used for the validation. If the schema is in the /io/schemas
        folder, the format name can be used (i.e. schema_path can be 'openlabel_v1' or
        'openlabel_v1_schema' to load the openlabel_v1_schema.json file). Default is
        'openlabel_v1'.

    Returns
    -------
    is_data_valid: bool
        True if the data validates against the schema, False if not.
    schema_errors: list of str
        All SchemaError messages found in the data. If the data is valid (if no SchemaErrors are
        found), this is an empty list.
    """

    # Since the schema_path can either be a complete path or the short name of a schema, these two
    # options must be distinguished. It is therefore assumed, that a complete path contains at #
    # least one '/' or '\'.

    if "/" in schema_path or "\\" in schema_path:  # if schema_path is a complete path
        schema_path = Path(schema_path)

    else:  # if schema_path is a schema name in /io/schemas
        local_schemas = [  # list of json files in /io/schemas
            p for p in os.listdir(Path(__file__).parent / "schemas") if p.endswith(".json")
        ]

        applicable_local_schemas = []  # list of possible schemas
        for local_schema_path in local_schemas:
            if schema_path in local_schema_path:
                applicable_local_schemas.append(local_schema_path)

        if len(applicable_local_schemas) == 1:  # if exactly one applicable file has been found
            schema_path = Path(__file__).parent / "schemas" / applicable_local_schemas[0]

        elif len(applicable_local_schemas) == 0:  # if no applicable files have been found

            err_msg = f"The key {schema_path} does not apply to any files in /io/schemas. Available schema files:"
            for p in local_schemas:
                err_msg += "\n - " + p

            raise FileNotFoundError(err_msg)

        else:  # if more than one applicable files have been found

            err_msg = f"The key {schema_path} applies to multiple files in /io/schemas:"
            for p in applicable_local_schemas:
                err_msg += "\n - " + p

            raise exceptions.AmbiguousSchemaNameError(err_msg)

    # Loads the schema data
    try:
        with schema_path.open() as schema_file:
            schema = json.load(schema_file)

    except FileNotFoundError:
        raise FileNotFoundError(f"The schema file could not be found in {schema_path}")

    # Validates the data
    validator = jsonschema.Draft7Validator(schema=schema)

    schema_errors = []
    for error in validator.iter_errors(data):
        schema_errors.append("$" + error.json_path[1:] + ": " + str(error.message))

    is_data_valid = len(schema_errors) == 0

    return is_data_valid, schema_errors
