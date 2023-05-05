# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import logging


def _warning(message: str) -> logging.Logger:
    """Create a loader warning."""
    logging.getLogger("loader_warnings").warning(message)
