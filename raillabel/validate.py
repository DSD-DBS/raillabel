# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import json
import os
import typing as t
from pathlib import Path

import fastjsonschema
import jsonschema

from . import exceptions


def validate(data: dict, schema_path: str = "raillabel_v2") -> t.Tuple[bool, t.List[str]]:
    """Validate JSON data represented by a dict via a given schema.

    Parameters
    ----------
    data: dict
        JSON data to be validated.
    schema_path: str, optional
        Path to the JSON schema used for the validation. If the schema is in the /schemas
        folder, the format name can be used (i.e. schema_path can be 'raillabel_v2' or
        'raillabel_v2_schema' to load the raillabel_v2_schema.json file). Default is
        'raillabel_v2'.

    Returns
    -------
    is_data_valid: bool
        True if the data validates against the schema, False if not.
    schema_errors: t.List of str
        All SchemaError messages found in the data. If the data is valid (if no SchemaErrors are
        found), this is an empty t.List.
    """

    # Since the schema_path can either be a complete path or the short name of a schema, these two
    # options must be distinguished. It is therefore assumed, that a complete path contains at #
    # least one '/' or '\'.

    if "/" in schema_path or "\\" in schema_path:  # if schema_path is a complete path
        schema_path = Path(schema_path)

    else:  # if schema_path is a schema name in /schemas
        local_schemas = [  # t.List of json files in /schemas
            p for p in os.listdir(Path(__file__).parent / "schemas") if p.endswith(".json")
        ]

        applicable_local_schemas = []  # t.List of possible schemas
        for local_schema_path in local_schemas:
            if schema_path in local_schema_path:
                applicable_local_schemas.append(local_schema_path)

        if len(applicable_local_schemas) == 1:  # if exactly one applicable file has been found
            schema_path = Path(__file__).parent / "schemas" / applicable_local_schemas[0]

        elif len(applicable_local_schemas) == 0:  # if no applicable files have been found

            err_msg = f"The key {schema_path} does not apply to a schema. Available schema files:"
            for p in local_schemas:
                err_msg += "\n - " + p

            raise FileNotFoundError(err_msg)

        else:  # if more than one applicable files have been found

            err_msg = f"The key {schema_path} applies to multiple files in /schemas:"
            for p in applicable_local_schemas:
                err_msg += "\n - " + p

            raise exceptions.AmbiguousSchemaNameError(err_msg)

    # Loads the schema data
    try:
        with schema_path.open() as schema_file:
            schema = json.load(schema_file)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"The schema file could not be found in {schema_path}") from e

    # Validates the data
    schema_errors = []

    try:
        # Use fastjsonschema since its faster (duh), and use jsonschema as a fallback if we find
        # an error to maintain jsonschemas way of reporting all errors
        fastjsonschema.validate(schema, data)
    except fastjsonschema.JsonSchemaException as _:
        validator = jsonschema.Draft7Validator(schema=schema)

        for error in validator.iter_errors(data):
            schema_errors.append("$" + error.json_path[1:] + ": " + str(error.message))

    is_data_valid = len(schema_errors) == 0

    return is_data_valid, schema_errors
