from dataclasses import dataclass
from typing import List, Optional
from .ostream import OStream, OStreamType
from .visualobject import VoPoint, VoVector, VoBox, VoImage, VoPolygon


@dataclass(repr=False)
class OStreamVisual(OStream):
    """
    A visual object stream is a stream of visual objects that are displayed on the screen.
    """
    refWidth: int = 1920
    refHeight: int = 1080
    points: Optional[List[VoPoint]] = None
    vectors: Optional[List[VoVector]] = None
    boxes: Optional[List[VoBox]] = None
    images: Optional[List[VoImage]] = None
    polygons: Optional[List[VoPolygon]] = None

    def __post_init__(self):
        self.oStreamType = OStreamType.VISUAL
