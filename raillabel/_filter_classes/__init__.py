# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Package containing the loader classes for all supported formats."""

from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules

# iterate through the modules in the current package
package_dir = str(Path(__file__).resolve().parent)
for (_, module_name, _) in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute):
            # Add the class to this package's variables
            globals()[attribute_name] = attribute
