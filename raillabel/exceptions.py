# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0


class MissingStreamError(Exception):
    """Raised when a coordinate system has no corresponding stream."""

    __module__ = "raillabel"


class MissingCoordinateSystemError(Exception):
    """Raised when a stream has no corresponding coordinate system."""

    __module__ = "raillabel"


class UnsupportedParentError(Exception):
    """Raised when a coordinate system does not have 'base' as parent."""

    __module__ = "raillabel"
