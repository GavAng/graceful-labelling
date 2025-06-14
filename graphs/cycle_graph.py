from collections.abc import Sequence
from itertools import pairwise
import networkx as nx
from typing import Self, override

from .utils import Vertex

from .directed_graph import DirectedGraph


class CycleGraph(DirectedGraph):
    @classmethod
    def from_vertices(
        cls, vertices: Sequence[Vertex], *, directed: bool = False
    ) -> Self:
        """
        if directed:
        else:
        """
        edges = pairwise(list(vertices) + [vertices[0]])
        if directed:
            return cls(vertices, list(edges))
        edges = [(i, j) if i < j else (j, i) for i, j in edges]
        return cls(vertices, edges)

    @classmethod
    @override
    def from_int(cls, n_vertices: int) -> Self:
        return cls.from_vertices(range(n_vertices), directed=True)

    @property
    @override
    def layout(self):
        return nx.circular_layout(self._graph)

    def draw(self):
        pi = 3
        super().draw(figsize=((self.n_vertices / pi) + 1, (self.n_vertices / pi) + 1))
