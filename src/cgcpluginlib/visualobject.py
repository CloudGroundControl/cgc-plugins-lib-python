from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from .jsonobject import JsonObject
from .general import LabelType, ColourIndexType, Marker


class VisualObjectType(str, Enum):
    POINT = "POINT"
    VECTOR = "VECTOR"
    BOX = "BOX"
    POLYGON = "POLYGON"
    IMAGE = "IMAGE"


@dataclass(repr=False)
class VoPoint(JsonObject):
    """
    A point is a visual object that is represented by a single point on the screen.
    """
    name: str = ""
    xmin: float = 0.0
    ymin: float = 0.0
    filterValue: Optional[float] = None
    clickable: Optional[str] = None
    labelType: Optional[LabelType] = None
    outlineColourIndex: Optional[ColourIndexType] = None
    marker: Optional[Marker] = None

    def __post_init__(self):
        self.visualObjectType = VisualObjectType.POINT


@dataclass(repr=False)
class VoVector(VoPoint):
    """
    A vector is a visual object that is represented by a line segment on the screen.
    """
    xmax: float = 0.0
    ymax: float = 0.0

    def __post_init__(self):
        self.visualObjectType = VisualObjectType.VECTOR


@dataclass(repr=False)
class VoBox(VoVector):
    """
    A box is a visual object that is represented by a rectangle on the screen.
    """
    fill: Optional[ColourIndexType] = None

    def __post_init__(self):
        self.visualObjectType = VisualObjectType.BOX


@dataclass(repr=False)
class VoImage(VoBox):
    """
    An image is a visual object that is represented by an image on the screen.
    """
    imageUrl: str = ""

    def __post_init__(self):
        self.visualObjectType = VisualObjectType.IMAGE


@dataclass(repr=False)
class VoVertex(JsonObject):
    x: float = 0.0
    y: float = 0.0


@dataclass(repr=False)
class VoPolygon(VoPoint):
    """
    A polygon is a visual object that is represented by a polygon on the screen.
    """
    triangleStripVertexes: Optional[List[VoVertex]] = None
    fill: Optional[ColourIndexType] = None

    def __post_init__(self):
        self.visualObjectType = VisualObjectType.POLYGON


@dataclass(repr=False)
class ClickPolygon(JsonObject):
    """
    A click polygon is a clickable polygon defined by a triangle strip.
    """
    triangleStripVertexes: Optional[List[VoVertex]] = None
    clickable: str = ""


@dataclass(repr=False)
class ClickBox(JsonObject):
    """
    A click box is a clickable box defined by a rectangle.
    """
    xmin: float = 0.0
    ymin: float = 0.0
    xmax: float = 0.0
    ymax: float = 0.0
    clickable: str = ""


@dataclass(repr=False)
class VoClickMap(JsonObject):
    """
    A click map is a collection of clickable polygons and boxes.
    """
    clickPolygons: Optional[List[ClickPolygon]] = None
    clickBoxes: Optional[List[ClickBox]] = None
