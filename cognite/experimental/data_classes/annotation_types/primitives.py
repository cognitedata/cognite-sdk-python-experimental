from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass
class Point:
    x: float
    y: float


PointDict = Dict[str, float]


def _process_vertices(vertices: List[Union[PointDict, Point]]) -> List[Point]:
    processed_vertices = []
    for v in vertices:
        if isinstance(v, Point):
            processed_vertices.push(v)
        elif isinstance(v, Dict) and v.keys() == ["x", "y"]:
            processed_vertices.push(Point(**v))
        else:
            raise ValueError(f"{v} is an invalid point.")
    return processed_vertices


@dataclass
class BoundingBox:
    x_min: float
    x_max: float
    y_min: float
    y_max: float


@dataclass
class CdfResourceRef:
    # A valid reference instance contains exactly one of these
    id: Optional[int] = None
    external_id: Optional[str] = None


@dataclass
class Polygon:
    # A valid polygon contains *at least* three vertices
    vertices: List[Point]

    def __post_init__(self) -> None:
        self.vertices = _process_vertices(self.vertices)


@dataclass
class PolyLine:
    # A valid polyline contains *at least* two vertices
    vertices: List[Point]

    def __post_init__(self) -> None:
        self.vertices = _process_vertices(self.vertices)
