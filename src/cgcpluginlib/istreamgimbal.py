from dataclasses import dataclass
from typing import Optional
from .istream import IStream, IStreamType
from .geo import Angular
import json


@dataclass(repr=False)
class IStreamGimbal(IStream):
    '''
    IStreamGimbal is the gimbal data received from the vehicle.
    '''
    gimbal: Optional[Angular] = None

    def __post_init__(self):
        self.iStreamType = IStreamType.GIMBAL


def parse_IStreamGimbal(file: str):
    '''
    Parse the IStreamBattery file.

    Parameters:
    - file: The IStreamBattery file.
    '''
    with open(file) as f:
        data = json.load(f)

        iStreamType = data.get('iStreamType', None)
        vehicleId = data.get('vehicleId', None)
        channelId = data.get('channelId', None)
        time = data.get('time', None)

        gimbal = data.get('gimbal', None)
        roll = gimbal['roll']
        pitch = gimbal['pitch']
        yaw = gimbal['yaw']

        istream_gimbal = IStreamGimbal(
            iStreamType=iStreamType,
            vehicleId=vehicleId,
            channelId=channelId,
            time=time,
            gimbal=Angular(
                roll=roll,
                pitch=pitch,
                yaw=yaw
            )
        )

        return istream_gimbal
