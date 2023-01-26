# Copyright DB Netz AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass

from .stream_calibration import StreamCalibration


@dataclass
class Stream:
    """A stream describes the source of a data sequence, usually a sensor.

    Parameters
    ----------
    uid: str
        Unique identifier of the stream. Commonly a friendly name.
    type: str
        A string encoding the type of the stream. The only valid values are 'camera', 'lidar',
        'radar', 'gps_imu' or 'other'.
    calibration: raillabel.format.StreamCalibration, optional
        Intrinsic calibration of the stream. Default is None.
    rostopic: str, optional
        The name of the rostopic of the stream. Default is None.
    description: str, optional
        Description of the stream. Default is None.
    """

    uid: str
    type: str
    calibration: StreamCalibration = None
    rostopic: str = None
    description: str = None

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

        dict_repr = {}

        if self.type is not None:
            dict_repr["type"] = str(self.type)

        if self.rostopic is not None:
            dict_repr["uri"] = str(self.rostopic)

        if self.description is not None:
            dict_repr["description"] = str(self.description)

        if self.calibration is not None:
            dict_repr["stream_properties"] = {"intrinsics_pinhole": self.calibration.asdict()}

        return dict_repr
