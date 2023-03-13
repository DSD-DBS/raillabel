..
   Copyright DB Netz AG and contributors
   SPDX-License-Identifier: Apache-2.0

=========================
3 Saving Annotation Files
=========================

If changes have been made to an annotation file or a file should be copied, it can be saved via the ``raillabel.save()`` method.

.. code-block:: python

    import raillabel

    scene = raillabel.load('path/to/file.json')
    scene.frames['0'].stream_stamps['lidar'].timestamp += 37
    raillabel.save(scene, 'path/to/file.json')

By default, the JSON file is saved as compact as possible with no linebreaks or indents. This can be changed by setting ``prettify_json=True`` as an argument. The indent size used is 4 spaces.

Validation
==========

If the data should be validated after beeing saved, the ``validate`` parameter can be set to True. If the data is not valid, a ``raillabel.SchemaError`` is raised with all errors included and the data is not saved.

.. code-block:: python

    import raillabel

    scene = raillabel.load('path/to/file.json')
    scene.frames['0'].stream_stamps['lidar'].timestamp += 37
    raillabel.save(scene, 'path/to/file.json', validate=True)
