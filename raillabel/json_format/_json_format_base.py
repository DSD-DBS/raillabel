# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel


class _JSONFormatBase(BaseModel, extra="forbid"):
    pass
