..
   Copyright DB Netz AG and contributors
   SPDX-License-Identifier: Apache-2.0

==========================
2 Loading Annotation Files
==========================

Loading annotation files into a raillabel.Scene is done with ``raillabel.load()``.

.. code-block:: python

    import raillabel
    scene = raillabel.load('path/to/file.json')

The method can itself identify if the file is from a supported format and then choose the correct loader-class.

Validation
==========
If the data should be validated before beeing loaded, the ``validate`` parameter can be set to True. If the data is not valid, a ``raillabel.SchemaError`` is raised with all errors included.

.. code-block:: python

    import raillabel
    scene = raillabel.load('path/to/file.json', validate=True)
