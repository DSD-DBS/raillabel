# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0


class UnsupportedFormatError(Exception):
    """Raised when a loaded annotation file is not in a supported format."""

    __module__ = "raillabel"


class SchemaError(Exception):
    """Raised when the data does not validate against a given schema."""

    __module__ = "raillabel"


class AmbiguousSchemaNameError(Exception):
    """Raised when a schema key applies to more than one schema files in.

    /io/schemas.
    """

    __module__ = "raillabel"
