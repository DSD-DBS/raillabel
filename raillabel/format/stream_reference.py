# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

import decimal
from dataclasses import dataclass
from typing import Optional

from .stream import Stream


@dataclass
class StreamReference:
    """A reference to a stream in a specific frame.

    Parameters
    ----------
    stream: raillabel.format.Stream
        The stream this StreamReference corresponds to.
    timestamp: decimal.Decimal
        Timestamp containing the Unix epoch time of the stream in a specific frame with up to
        nanosecond precision.
    uri: str, optional
        URI to the file corresponding to the frame recording in the particular frame. Default is
        None.
    """

    stream: Stream
    timestamp: decimal.Decimal
    uri: Optional[str] = None

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

        dict_repr = {"stream_properties": {"stream_sync": {"timestamp": str(self.timestamp)}}}

        if self.uri is not None:
            dict_repr["uri"] = self.uri

        return dict_repr
