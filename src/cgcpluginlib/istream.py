from dataclasses import dataclass
from enum import Enum
from typing import Optional
from cgcpluginlib import JsonObject


class IStreamType(str, Enum):
    BASE = "BASE"
    GIMBAL = "GIMBAL"
    BATTERY = "BATTERY"
    GEOLOCATION = "GEOLOCATION"
    SIGNAL_STRENGTH = "SIGNAL_STRENGTH"
    VIDEO_STREAM = "VIDEO_STREAM"
    VIDEO_FRAME = "VIDEO_FRAME"
    CUSTOM_USER = "CUSTOM_USER"


@dataclass(repr=False)
class IStream(JsonObject):
    """
    Base class for all IStream types.
    """
    iStreamType: IStreamType = IStreamType.BASE
    vehicleId: Optional[str] = None
    channelId: Optional[str] = None
    time: Optional[str] = None
