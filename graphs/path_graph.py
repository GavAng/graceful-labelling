from collections.abc import Sequence
from itertools import pairwise
from typing import Self, override

from .directed_graph import DirectedGraph
from .utils import Position, Vertex


class PathGraph(DirectedGraph):
    @classmethod
    @override
    def from_vertices(
        cls, vertices: Sequence[Vertex], *, directed: bool = False
    ) -> Self:
        """
        if directed:
            Creates a directed path graph of len(vertices) nodes with vertex labels
            vertices[0], vertex[1], ..., vertex[-1] and edges oriented forwards.
        else:
            Creates a directed path graph of len(vertices) nodes with vertex labels
            vertices[0], vertex[1], ..., vertex[-1] and edges oriented from the smaller
            vertex to the larger.
        """
        edges = pairwise(vertices)
        if directed:
            return cls(vertices, list(edges))
        edges = [(i, j) if i < j else (j, i) for i, j in edges]
        return cls(vertices, edges)

    @property
    @override
    def layout(self) -> dict[Vertex, Position]:
        return {vertex: (i, 0) for i, vertex in enumerate(self.vertices)}

    def draw(self):
        super().draw(figsize=(self.n_vertices, 1))
