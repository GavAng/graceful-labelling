from itertools import chain
import math
from typing import TypeVar, TypedDict, override

from .directed_graph import DirectedGraph
from .path_graph import PathGraph
from .utils import Edge, Position, Vertex

T = TypeVar("T")


class ForkGraphArgs(TypedDict):
    path: PathGraph
    ends: tuple[Edge, Edge]


class ForkGraph(DirectedGraph):
    def __init__(self, path: PathGraph, ends: tuple[Edge, Edge]):
        super().from_edges(chain(path.edges, ends))
        ends_common = set(ends[0]) & set(ends[1])
        connector = next(iter(ends_common))
        if path.vertices[0] == connector:
            path = PathGraph(list(reversed(path.vertices)), path.edges)
        self.path = path
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

    def draw(self):
        super().draw(figsize=(self.n_vertices, 2))
