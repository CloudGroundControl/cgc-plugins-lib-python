from dataclasses import dataclass
from enum import Enum
from typing import Optional
from .jsonobject import JsonObject


class OStreamType(str, Enum):
    BASE = "BASE"
    VISUAL = "VISUAL"
    GEOINFO = "GEOINFO"
    SCALAR = "SCALAR"
    HEATMAP = "HEATMAP"
    ALPHABITMAP = "ALPHABITMAP"


@dataclass(repr=False)
class OStream(JsonObject):
    """
    Base class for all OStream types.
    """
    oStreamType: OStreamType = OStreamType.BASE
    desc: str = ""
    imageUrl: Optional[str] = None
