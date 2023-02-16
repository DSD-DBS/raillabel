# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import typing as t
from abc import ABC, abstractmethod, abstractproperty

from ..format._annotation import _Annotation
from ..format.frame import Frame


class _FilterABC(ABC):
    """ABC for all filter classes.

    Creating a new filter
    ---------------------
    To create a new, custom filter create a new class in this dir, that inherits from _FilterABC. Any class, that inherits from _FilterABC will automatically be loaded by the filter function.
    Include the filter arguments (include_[...], exclude_[...], ...) in the PARAMETERS field. These will be mutually exclusive.
    Select a level for the filter. The level determines where the filter is going to be applied (e.g. at the frame level, annotation level, ...).
    Include the conditions to pass the filter in the passes_filter() method, which returns True if the filter is passed.
    The contents of the filter arguments can optionally be processed by the _process_filter_args().
    """

    @property
    @abstractproperty
    def PARAMETERS(self) -> t.List[str]:
        raise NotImplementedError

    @property
    @abstractproperty
    def LEVELS(self) -> t.List[str]:
        raise NotImplementedError

    def __init__(self, kwargs):

        set_parameter = None
        for param in self.PARAMETERS:
            if param in kwargs and param is not None:

                if set_parameter is None:
                    setattr(self, param, self._process_filter_args(kwargs[param]))
                    set_parameter = param
                else:
                    raise ValueError(
                        f"{set_parameter} and {param} are mutually exclusive, but were both set."
                    )

            else:
                setattr(self, param, None)

    @abstractmethod
    def passes_filter(self, annotation: t.Union[t.Type[_Annotation], Frame]) -> bool:
        raise NotImplementedError

    def _process_filter_args(self, filter_args):
        """Process filter arguments (optional)."""
        return filter_args
