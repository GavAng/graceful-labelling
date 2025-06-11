from collections.abc import Sequence
import networkx as nx
from typing import TypeVar, override

from .base_graph import BaseGraph
from .utils import Vertex

T = TypeVar("T")


class PathGraph(BaseGraph):
    @classmethod
    def from_vertices(cls, vertices: Sequence[Vertex]):
        """
        Creates a directed path graph of len(vertices) nodes with vertex labels
        vertices[0], vertex[1], ..., vertex[-1].
        """
        return cls.from_graph(nx.path_graph(vertices))

    @classmethod
    def from_int(cls, n_nodes: int):
        """
        Creates a directed path graph of n_nodes nodes with vertex labels 0, 1, ..., n_nodes-1.
        """
        return cls.from_vertices(range(n_nodes))

    @property
    @override
    def layout(self):
        return {vertex: (i, 0) for i, vertex in enumerate(self.vertices)}
