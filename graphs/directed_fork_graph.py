from collections.abc import Collection, Iterable, Sequence
from itertools import pairwise
import math
from typing import Self, override

from .directed_graph import DirectedGraph
from .directed_path_graph import DirectedPathGraph
from .utils import Edge, Position, Vertex


class DirectedForkGraph(DirectedGraph):
    def __init__(self, vertices: Iterable[Vertex], edges: Collection[Edge]):
        super().__init__(vertices, edges)
        *path_vertices, end_vertex_1, end_vertex_2 = vertices
        *path_edges, _, _ = edges

        self.path = DirectedPathGraph(path_vertices, path_edges)
        self.ends = (end_vertex_1, end_vertex_2)

    @classmethod
    @override
    def from_vertices(cls, vertices: Sequence[Vertex]) -> Self:
        *path_vertices, end_vertex_1, end_vertex_2 = vertices
        connector = path_vertices[-1]
        end_edge_1 = (connector, end_vertex_1)
        end_edge_2 = (connector, end_vertex_2)
        edges = [
            (i, j) if i < j else (j, i)
            for i, j in list(pairwise(path_vertices)) + [end_edge_1, end_edge_2]
        ]
        return cls(vertices, edges)

    @classmethod
    def from_path_vertices(
        cls, path: Sequence[Vertex], ends: tuple[Vertex, Vertex]
    ) -> Self:
        return cls.from_vertices(list(path) + list(ends))

    @property
    @override
    def layout(self):
        layout: dict[Vertex, Position] = {
            vertex: (i, 0) for i, vertex in enumerate(self.path.vertices)
        }
        for i, end in enumerate(self.ends):
            x = len(self.path.vertices) - 1 + (1 / math.sqrt(2))
            y = (-1) ** i * (1 / math.sqrt(2))
            layout[end] = (x, y)
        return layout

    def draw(self):
        super().draw(figsize=(self.n_vertices, 2))
