..
   Copyright DB InfraGO AG and contributors
   SPDX-License-Identifier: Apache-2.0

*****************************
Welcome to the documentation!
*****************************

Python RailLabel Development-Kit
================================

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black

**Date**: |today| **Version**: |Version|

..
   Copyright DB InfraGO AG and contributors
   SPDX-License-Identifier: Apache-2.0


Description
-----------
This library is designed to assist in the handling of the sensor annotations of Deutsche Bahn in the OpenLABEL data format. Common usage for the library:

* fetching specific information from annotation files
* filtering for specific frames, annotations or objects
* editing annotation files

Motivation
----------

Working with our own data has brought up the need to interact with the annotations programmatically. The annotation data is stored in .json files in the `ASAM OpenLABEL annotation <https://www.asam.net/standards/detail/openlabel/>`_ format, an emerging industry standard targeted towards the automotive sector. But as a standard it is designed very inclusively, which makes it overloaded for our limited use cases. We therefore decided to create a submodel called "RailLabel" with a corresponding devkit for easier interaction with the data. The example below shows a comparison between a purely JSON based approach compared to the devkit.

With JSON only:

.. code-block:: python

    import json

    with open('path/to/file.json', 'r') as data_file:
        scene = json.load(data_file)

    scene['openlabel']['frames']['1']['frame_properties']['streams']['lidar']['stream_properties']['stream_sync']['timestamp'] += 37

    with open('path/to/other_file.json', 'w') as data_file:
        json.dump(scene, data_file)

With RailLabel:

.. code-block:: python

    import raillabel

    scene = raillabel.load('path/to/file.json')
    scene.frames[1].sensors['lidar'].timestamp += 37
    raillabel.save(scene, 'path/to/other_file.json')

Content
-------

.. toctree::
   :caption: Modules
   :maxdepth: 4

   code/modules
