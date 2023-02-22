# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass


@dataclass
class Object:
    """Physical, unique object in the data, that can be tracked via its UID.

    Parameters
    ----------
    uid: str
        This a string representing the unique universal identifier for the object.
    name: str
        Name of the object. It is a friendly name and not used for indexing. Commonly the class
        name is used followed by an underscore and an integer (i.e. person_0032).
    type: str
        The type of an object defines the class the object corresponds to.
    """

    uid: str
    name: str
    type: str

    def asdict(self) -> dict:
        """Export self as a dict compatible with the OpenLABEL schema.

        Returns
        -------
        dict_repr: dict
            Dict representation of this class instance.

        Raises
        ------
        ValueError
            if an attribute can not be converted to the type required by the OpenLabel schema.
        """

        return {"name": str(self.name), "type": str(self.type)}
