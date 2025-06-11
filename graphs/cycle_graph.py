from collections.abc import Sequence
import networkx as nx
from typing import TypeVar, override

from .utils import Vertex

from .directed_graph import DirectedGraph

T = TypeVar("T")


class CycleGraph(DirectedGraph):
    @classmethod
    def from_vertices(cls, vertices: Sequence[Vertex]):
        """
        Creates a directed cycle graph of len(vertices) nodes with vertex labels in order round the circle
        vertices[0], vertex[1], ..., vertex[-1].
        """
        return cls.from_graph(nx.cycle_graph(vertices))

    @classmethod
    def from_int(cls, n_nodes: int):
        """
        Creates a directed cycle graph of n_nodes nodes with vertex labels in order round the circle
        0, 1, ..., n_nodes-1.
        """
        return cls.from_vertices(range(n_nodes))

    @property
    @override
    def layout(self):
        return nx.circular_layout(self._graph)
