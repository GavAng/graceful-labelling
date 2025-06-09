from abc import ABC
from collections.abc import Collection
import matplotlib.pyplot as plt
import networkx as nx
from typing import TypeVar

from .utils import Edge

T = TypeVar("T")


class BaseGraph(ABC):
    def __init__(self, edges: Collection[Edge]) -> None:
        graph = nx.DiGraph(edges)
        self._graph = graph

    @classmethod
    def from_graph(cls, graph: nx.Graph):
        """
        Converts an undirected NetworkX Graph G to a DiGraph D under the orientation (i, j) in V(D)
        if and only if {i, j} in V(G) and i < j.
        """
        return cls(graph.edges)

    @property
    def edge_labels(self) -> dict[Edge, int]:
        return {edge: self.get_edge_label(edge) for edge in self.edges}

    def get_edge_label(self, edge: Edge) -> int:
        return (edge[1] - edge[0]) % (self.n_edges + 1)

    @property
    def vertices(self) -> list[int]:
        return list(self._graph.nodes)

    @property
    def edges(self) -> list[Edge]:
        return list(self._graph.edges)

    @property
    def n_edges(self) -> int:
        return len(self.edges)

    def get_layout(self):
        return nx.spring_layout(self._graph)

    def draw(self, layout=None, seed: int | None = None) -> None:
        if layout is None:
            layout = self.get_layout()
        nx.draw(
            self._graph,
            pos=layout,
            with_labels=True,
            node_color="lightblue",
        )
        nx.draw_networkx_edge_labels(
            self._graph,
            pos=layout,
            edge_labels=self.edge_labels,
        )
        plt.show()
