from dataclasses import dataclass
import json
from typing import Optional
from .istream import IStream, IStreamType
from .geo import GeoLocation, GeoLocationBase, Angular


@dataclass(repr=False)
class IStreamGeoLocation(IStream):
    '''
    IStreamGeoLocation is received from the vehicle and contains the current location of the vehicle.
    '''
    position: Optional[GeoLocation] = None
    velocity: Optional[GeoLocation] = None

    def __post_init__(self):
        self.iStreamType = IStreamType.GEOLOCATION


def parse_IStreamGeoLocation(file: str):
    '''
    Parse the IStreamGeoLocation file.

    Parameters:
    - file: The IStreamGeoLocation file.
    '''
    with open(file) as f:
        data = json.load(f)

        iStreamType = data.get('iStreamType', None)
        vehicleId = data.get('vehicleId', None)
        channelId = data.get('channelId', None)
        time = data.get('time', None)

        position = data.get('position', None)
        velocity = data.get('velocity', None)

        if position is not None:
            position = GeoLocation(
                geolocation=GeoLocationBase(
                    latitude=position['geolocation']['latitude'],
                    longitude=position['geolocation']['longitude'],
                    altitude=position['geolocation']['altitude']
                ),
                angular=Angular(
                    roll=position['angular']['roll'],
                    pitch=position['angular']['pitch'],
                    yaw=position['angular']['yaw']
                )
            )

        if velocity is not None:
            velocity = GeoLocation(
                geolocation=GeoLocationBase(
                    latitude=velocity['geolocation']['latitude'],
                    longitude=velocity['geolocation']['longitude'],
                    altitude=velocity['geolocation']['altitude']
                ),
                angular=Angular(
                    roll=velocity['angular']['roll'],
                    pitch=velocity['angular']['pitch'],
                    yaw=velocity['angular']['yaw']
                )
            )

        istream_geolocation = IStreamGeoLocation(
            iStreamType=iStreamType,
            vehicleId=vehicleId,
            channelId=channelId,
            time=time,
            position=position,
            velocity=velocity
        )

    return istream_geolocation
