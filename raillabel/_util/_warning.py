# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import logging
import typing as t
from io import StringIO


class _WarningsLogger:

    warnings: t.List[str] = []

    def __enter__(self) -> "_WarningsLogger":
        logger = logging.getLogger("loader_warnings")
        warnings_stream = StringIO()
        handler = logging.StreamHandler(warnings_stream)
        handler.setLevel(logging.WARNING)
        logger.addHandler(handler)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logger = logging.getLogger("loader_warnings")
        stream = logger.handlers[-1].stream
        stream.seek(0)

        warnings_list = stream.getvalue().split("\n")

        if len(warnings_list) > 0:
            warnings_list = warnings_list[:-1]

        self.warnings = warnings_list


def _warning(message: str) -> logging.Logger:
    """Create a loader warning."""
    logging.getLogger("loader_warnings").warning(message)
