from collections.abc import Iterable, Sequence
from itertools import pairwise
from typing import TypeVar, override

from .directed_graph import DirectedGraph
from .utils import Edge, Position, Vertex

T = TypeVar("T")


class PathGraph(DirectedGraph):
    def __init__(self, ordered_vertices: Sequence[Vertex], edges: Iterable[Edge]):
        super().__init__(ordered_vertices, edges)

    @classmethod
    def from_vertices_directed(cls, vertices: Sequence[Vertex]):
        """
        Creates a directed path graph of len(vertices) nodes with vertex labels
        vertices[0], vertex[1], ..., vertex[-1] and edges oriented forwards.
        """
        return cls(vertices, pairwise(vertices))

    @classmethod
    def from_vertices_standard(cls, vertices: Sequence[Vertex]):
        """
        Creates a directed path graph of len(vertices) nodes with vertex labels
        vertices[0], vertex[1], ..., vertex[-1] and edges oriented from the smaller
        vertex to the larger.
        """
        edges = [(i, j) if i < j else (j, i) for i, j in pairwise(vertices)]
        return cls(vertices, edges)

    # @classmethod
    # def from_int(cls, n_nodes: int):
    #     """
    #     Creates a directed path graph of n_nodes nodes with vertex labels 0, 1, ..., n_nodes-1.
    #     """
    #     return cls.from_vertices(range(n_nodes))

    @property
    @override
    def layout(self) -> dict[Vertex, Position]:
        return {vertex: (i, 0) for i, vertex in enumerate(self.vertices)}

    def draw(self):
        super().draw(figsize=(self.n_edges, 1))
