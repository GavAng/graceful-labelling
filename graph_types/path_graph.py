from collections.abc import Sequence
from itertools import pairwise
from typing import TypeVar, override

from graph_types.base_graph import BaseGraph

T = TypeVar("T")


class PathGraph(BaseGraph):
    @classmethod
    def from_vertices(cls, vertices: Sequence[int]):
        return cls(list(pairwise(vertices)))

    @classmethod
    def from_int(cls, n_nodes: int):
        return cls.from_vertices(range(n_nodes))

    @override
    def get_layout(self):
        return {vertex: (i, 0) for i, vertex in enumerate(self.vertices)}
