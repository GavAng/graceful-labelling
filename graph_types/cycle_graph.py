from collections.abc import Sequence
from itertools import pairwise
import networkx as nx
from typing import TypeVar, override

from graph_types.base_graph import BaseGraph

T = TypeVar("T")


class CycleGraph(BaseGraph):
    @classmethod
    def from_vertices(cls, vertices: Sequence[int]):
        if not vertices:
            return cls([])
        start = vertices[0]
        return cls(list(pairwise(list(vertices) + [start])))

    @classmethod
    def from_int(cls, n_nodes: int):
        return cls.from_vertices(range(n_nodes))

    @override
    def get_layout(self):
        return nx.circular_layout(self._graph)
