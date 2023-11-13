from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from cgcpluginlib import JsonObject
from cgcpluginlib import LabelType, ColourIndexType, Marker


class GeoInfoType(str, Enum):
    POINT = "POINT"
    LINK = "LINK"


@dataclass(repr=False)
class GeoLocationBase(JsonObject):
    '''
      - latitude: Unit 1e-7 degree.
      - longitude: Unit 1e-7 degree.
      - altitude: Unit is cm.
    '''
    latitude: int = 0
    longitude: int = 0
    altitude: int = 0


@dataclass(repr=False)
class Angular(JsonObject):
    '''
    Unit 0.01 degree. From -18000 to 18000.

    Attributes:
      - roll: 0 is horizontal
      - pitch: 0 is horizontal
      - yaw: 0 is North
    '''
    roll: int = 0
    pitch: int = 0
    yaw: int = 0


@dataclass(repr=False)
class GeoLocation(JsonObject):
    '''
    GeoLocation contains the geolocation and angular information of a point.
    '''
    geolocation: Optional[GeoLocationBase] = None
    angular: Optional[Angular] = None


@dataclass(repr=False)
class GeoInfo(JsonObject):
    '''
    GeoInfo contains information about a single point. If the geoInfoType is LINKED, the GeoInfo will be linked to the previous GeoInfo if it is in a GeoInfo list.
    '''
    position: GeoLocation = GeoLocation()
    velocity: GeoLocation = GeoLocation()
    geoInfoType: GeoInfoType = GeoInfoType.POINT
    imageUrl: Optional[str] = None
    clickable: Optional[str] = None
    marker: Optional[Marker] = None


@dataclass(repr=False)
class GeoPolygon(JsonObject):
    '''
    GeoPolygon contains information about a polygon. It is used to represent a polygon on the map.
    '''
    name: str = ""
    labelType: LabelType = LabelType.P
    outline: ColourIndexType = ColourIndexType.C15
    fill: ColourIndexType = ColourIndexType.C0
    positions: Optional[List[GeoLocationBase]] = None
    imageUrl: Optional[str] = None
    clickable: Optional[str] = None
