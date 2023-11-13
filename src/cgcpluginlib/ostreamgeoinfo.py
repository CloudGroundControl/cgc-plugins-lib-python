from dataclasses import dataclass
from typing import List, Optional
from cgcpluginlib import OStream, OStreamType
from cgcpluginlib import GeoInfo, GeoPolygon


@dataclass(repr=False)
class OStreamGeoInfos(OStream):
    '''
    OStreamGeoInfos are used to send GeoInfo and/or GeoPolygon to the map.
    '''
    desc: str = ""
    geoInfos: Optional[List[GeoInfo]] = None
    geoPolygons: Optional[List[GeoPolygon]] = None
    imageUrl: Optional[str] = None

    def __post_init__(self):
        self.oStreamType = OStreamType.GEOINFO
