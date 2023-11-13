from dataclasses import dataclass
from typing import Optional
from .istream import IStream, IStreamType
import json


@dataclass(repr=False)
class IStreamSignalStrength(IStream):
    '''
    IStreamSignalStrength is the signal strength data received from the vehicle.
    '''
    level: Optional[int] = None
    dbm: Optional[int] = None
    standard: Optional[str] = None
    uplink: Optional[int] = None
    downlink: Optional[int] = None

    def __post_init__(self):
        self.iStreamType = IStreamType.SIGNAL_STRENGTH


def parse_IStreamSignalStrength(file: str):
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

        level = data.get('level', None)
        dbm = data.get('dbm', None)
        standard = data.get('standard', None)
        uplink = data.get('uplink', None)
        downlink = data.get('downlink', None)

        istream_gimbal = IStreamSignalStrength(
            iStreamType=iStreamType,
            vehicleId=vehicleId,
            channelId=channelId,
            time=time,
            level=level,
            dbm=dbm,
            standard=standard,
            uplink=uplink,
            downlink=downlink
        )

        return istream_gimbal
