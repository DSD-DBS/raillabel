# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations


def _empty_list_to_none(collection: list | None) -> list | None:
    if collection is None:
        return None
    if len(collection) == 0:
        return None
    return collection


def _flatten_list(list_of_tuples: list[tuple]) -> list:
    return [item for tup in list_of_tuples for item in tup]
