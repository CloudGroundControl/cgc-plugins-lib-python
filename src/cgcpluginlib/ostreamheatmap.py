from dataclasses import dataclass
from typing import Optional
from .jsonobject import JsonObject
from .ostream import OStream, OStreamType
from .visualobject import VoClickMap


@dataclass(repr=False)
class HeatmapInfo(JsonObject):
    '''
    A HeatmapInfo object represents the heatmap configuration.
    '''
    scalingFactor: Optional[float] = 100.0
    scalingUnit: Optional[str] = None


@dataclass(repr=False)
class OStreamHeatmap(OStream):
    """
    An OStreamHeatmap is used to display a images as a live heatmap on top of the video stream.
    """
    heatmapInfo: Optional[HeatmapInfo] = None
    clickMap: Optional[VoClickMap] = None

    def __post_init__(self):
        self.oStreamType = OStreamType.HEATMAP
