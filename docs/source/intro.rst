..
   Copyright DB Netz AG and contributors
   SPDX-License-Identifier: Apache-2.0

Motivation
----------

Working with our own data has brought up the need to interact with the annotations programmatically. The annotation data is stored in .json files in the `ASAM OpenLABEL annotation <https://www.asam.net/standards/detail/openlabel/>`_ format, an emerging industry standard targeted towards the automotive sector. But as a standard it is designed very inclusively, which makes it overloaded for our limited use cases. We therefore decided to create a submodel called "RailLabel" with a corresponding devkit for easier interaction with the data. The example below shows a comparison between a purely JSON based approach compared to the devkit.

With JSON only:

.. code-block:: python

    import json

    with open('path/to/file.json', 'r') as data_file:
        scene = json.load(data_file)

    scene['openlabel']['frames']['0']['frame_properties']['streams']['lidar']['stream_properties']['stream_sync']['timestamp'] += 37

    with open('path/to/other_file.json', 'w') as data_file:
        json.dump(scene, data_file)

With RailLabel:

.. code-block:: python

    import raillabel

    scene = raillabel.load('path/to/file.json')
    scene.frames['0'].streams['lidar'].timestamp += 37
    raillabel.save(scene, 'path/to/other_file.json')


The devkit also includes other functionality like validating data against a schema and filtering the annotations.
