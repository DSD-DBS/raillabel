# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""Configuration file for Sphinx."""


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

import raillabel

# -- Project information -----------------------------------------------------

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]
with open("../../pyproject.toml", "rb") as f:
    _metadata = tomllib.load(f)["project"]

project = "RailLabel"
pypi = "raillabel"
author = _metadata["authors"][0]["name"]
copyright = f"{author} and the {_metadata['name']} contributors"
license = _metadata["license"]["text"]
install_requirements = _metadata["dependencies"]
python_requirement = _metadata["requires-python"]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = []


# -- General information about the project -----------------------------------

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# The full version, including alpha/beta/rc tags.
version = raillabel.__version__
rst_epilog = """
.. |Project| replace:: {project}
.. |Version| replace:: {version}
""".format(
    project=project, version=version
)


# -- Options for copy-button -------------------------------------------------
copybutton_here_doc_delimiter = "EOT"
copybutton_line_continuation_character = "\\"


# -- Options for auto-doc ----------------------------------------------------
autoclass_content = "class"


# -- Options for napoleon ----------------------------------------------------
napoleon_google_docstring = False
napoleon_include_init_with_doc = True


# -- Options for Intersphinx output ------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "furo"
html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/DSD-DBS/raillabel",
            "html": '<img src="/_static/img/github-logo.svg"/>',
            "class": "",
        },
    ],
}


# -- Extra options for Furo theme --------------------------------------------

pygments_style = "tango"
pygments_dark_style = "monokai"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
