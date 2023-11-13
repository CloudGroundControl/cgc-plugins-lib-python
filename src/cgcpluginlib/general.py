from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Optional

from cgcpluginlib import JsonObject


class LabelType(str, Enum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    P = "p"


class ColourIndexType(IntEnum):
    C0 = 0
    C1 = 1
    C2 = 2
    C3 = 3
    C4 = 4
    C5 = 5
    C6 = 6
    C7 = 7
    C8 = 8
    C9 = 9
    C10 = 10
    C11 = 11
    C12 = 12
    C13 = 13
    C14 = 14
    C15 = 15


class MarkerType(str, Enum):
    ARROW = "ARROW"
    BOX = "BOX"
    CROSS = "CROSS"
    X = "X"
    STAR = "STAR"
    CIRCLE = "CIRCLE"
    TRIANGLE = "TRIANGLE"


@dataclass(repr=False)
class Marker(JsonObject):
    '''
    Marker for GeoInfo.
      - bearing: The bearing of the marker in degrees. Unit 0.01 degree. From -18000 to 18000. 0 is North.
    '''
    type: MarkerType = MarkerType.ARROW
    bearing: Optional[float] = None
