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

    /schemas.
    """

    __module__ = "raillabel"


class MissingStreamError(Exception):
    """Raised when a coordinate system has no corresponding stream."""

    __module__ = "raillabel"


class MissingCoordinateSystemError(Exception):
    """Raised when a stream has no corresponding coordinate system."""

    __module__ = "raillabel"


class UnsupportedParentError(Exception):
    """Raised when a coordinate system does not have 'base' as parent."""

    __module__ = "raillabel"
