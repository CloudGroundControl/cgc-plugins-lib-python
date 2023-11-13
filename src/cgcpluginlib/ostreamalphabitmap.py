from dataclasses import dataclass
from typing import Optional
from .jsonobject import JsonObject
from .ostream import OStream, OStreamType
from .visualobject import VoClickMap


@dataclass(repr=False)
class OStreamAlphaBitMap(OStream):
    """
    An OStreamAlphaBitMap is used to display images on top of the video stream.
    """
    imageUrl: Optional[str] = None
    clickMap: Optional[VoClickMap] = None

    def __post_init__(self):
        self.oStreamType = OStreamType.ALPHABITMAP
