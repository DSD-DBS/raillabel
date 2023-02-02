..
   Copyright DB Netz AG and contributors
   SPDX-License-Identifier: Apache-2.0

==================
4 Filtering Scenes
==================

The annotations of a scene can be filtered by many criteria. This functionality is provided by ``raillabel.filter()``. This method takes a scene and filter arguments and returns a copy of the scene with filters applied.

.. code-block:: python

    import raillabel
    import decimal

    scene = raillabel.load('path/to/file.json')

    scene_with_only_trains = raillabel.filter(
        scene,
        include_classes='train'
    )
    scene_without_bboxs = raillabel.filter(
        scene,
        exclude_annotation_types=['bbox']
    )
    cut_scene_with_only_red_trains = raillabel.filter(
        scene,
        start_timestamp=decimal.Decimal('1587349200.004200000'),
        exclude_frames=[4, 2],
        include_classes='train',
        include_attributes={
            'color': 'red'
        }
    )
    scene_with_annotations_with_an_attribute = raillabel.filter(
        scene,
        include_attributes={ # All annotations with the color
            'color': None    # attribute will be included,
        }                    # regardless of color value.
    )

Most filter categories have an include and exclude parameter (i.e ``include_classes`` and ``exclude_classes``). When include is set, all annotations, that meet the criterium are *included* into the filtered scene. Excluded parameters are *excluded* from the scene. These two parameters are mutually exclusive and can not both be set.

.. code-block:: python

    invalid_scene = raillabel.filter(
        scene,
        include_classes='person',  # Will raise a ValueError due
        exclude_classes='train'    # to mutual exclusivity.
    )
