from collections.abc import Sequence
import math
from typing import TypeVar, override

from .base_graph import BaseGraph
from .path_graph import PathGraph
from .utils import Edge, Position, Vertex

T = TypeVar("T")


class ForkGraph(BaseGraph):
    @override
    def __init__(self, path: Sequence[Edge], ends: tuple[Edge, Edge]):
        super().__init__(list(path) + list(ends))
        self.path = PathGraph(path)
        self.ends = ends

    @property
    @override
    def layout(self):
        layout: dict[Vertex, Position] = {
            vertex: (i, 0) for i, vertex in enumerate(self.path.vertices)
        }
        connector = self.path.vertices[-1]
        for i, edge in enumerate(self.ends):
            endpoint = self.get_other_endpoint(edge, connector)
            x = len(self.path.vertices) - 1 + (1 / math.sqrt(2))
            y = (-1) ** i * (1 / math.sqrt(2))
            layout[endpoint] = (x, y)
        return layout
