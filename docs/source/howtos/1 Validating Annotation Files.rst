..
   Copyright DB Netz AG and contributors
   SPDX-License-Identifier: Apache-2.0

=============================
1 Validating Annotation Files
=============================

Some annotation files might not fit the valid schema, depending on their source and editing history. To check whether a JSON file is a valid RailLabel annotation file, the raillabel.validate() method can be used. This checks the JSON file against a given schema and returns whether the data is valid and any potential incompatibilities with the schema.

.. code-block:: python

    import raillabel

    valid_data = {
        "openlabel": {
            "metadata": {
                "schema_version": "1.0.0"
            }
        }
    }

    raillabel.validate(valid_data)

.. code-block:: python

    Returns: (True, [])

.. code-block:: python

    import raillabel

    invalid_data = {
        "openlabel": {
            "metadata": {
                "schema_version": "1.0.0"
            },
            "invalid_field": "foo"
        }
    }

    raillabel.validate(invalid_data)

.. code-block:: python

    Returns: (False, ["$.openlabel: Additional properties are not allowed ('invalid_field' was unexpected)"])

By default, the OpenLABEL JSON schema is used for validation. However, the method can validate data with any schema.

.. code-block:: python

    import raillabel

    data = {
        "openlabel": {
            "metadata": {
                "schema_version": "2.0.0"
            }
        }
    }

    raillabel.validate(data, "path/to/schema.json")

The method returns a tuple of two elements. The first element is a boolean marking if the data validates against the schema. The second is a list of strings with each string being an error in the data. This example shows how to present the results of the method to a user.

.. code-block:: python

    is_data_valid, warnings = raillabel.validate(data)

    if is_data_valid:
        do_something()

    else:
        for w in warnings:
            print(w)
