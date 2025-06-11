from collections.abc import Iterable
from itertools import chain
import matplotlib.pyplot as plt
import networkx as nx
from typing import TypeVar

from .utils import Edge, Position, Vertex

T = TypeVar("T")


class DirectedGraph:
    def __init__(self, vertices: Iterable[Vertex], edges: Iterable[Edge]) -> None:
        edge_vertices = chain.from_iterable(edges)
        if not set(edge_vertices).issubset(vertices):
            raise ValueError("An edge contains an endpoint not in the vertex set.")

        graph = nx.DiGraph()
        graph.add_nodes_from(vertices)
        graph.add_edges_from(edges)
        self._graph = graph

    @classmethod
    def from_edges(cls, edges: Iterable[Edge]):
        vertices = set(chain.from_iterable(edges))
        return DirectedGraph(vertices, edges)

    @classmethod
    def from_graph(cls, graph: nx.Graph):
        """
        Converts an undirected NetworkX Graph G to a DiGraph D under the orientation (i, j) in V(D)
        if and only if {i, j} in V(G) and i < j.
        """
        return DirectedGraph.from_edges(graph.edges)

    @property
    def edge_labels(self) -> dict[Edge, int]:
        return {edge: self.get_edge_label(edge) for edge in self.edges}

    def get_edge_label(self, edge: Edge) -> int:
        return (edge[1] - edge[0]) % (self.n_edges + 1)

    @property
    def vertices(self) -> list[Vertex]:
        return list(self._graph.nodes)

    @property
    def n_vertices(self) -> int:
        return len(self.vertices)

    @property
    def edges(self) -> list[Edge]:
        return list(self._graph.edges)

    @property
    def n_edges(self) -> int:
        return len(self.edges)

    def add_edge(self, edge: Edge) -> None:
        u, v = edge
        self._graph.add_edge(u, v)

    def get_degree(self, vertex: Vertex) -> int:
        return self._graph.degree[vertex]

    def get_other_endpoint(self, edge: Edge, vertex: Vertex) -> Vertex:
        if vertex in edge:
            return edge[(edge.index(vertex) + 1) % 2]
        raise ValueError("Given edge does not contain given vertex.")

    def contains_edge(self, edge: Edge, directed: bool = True) -> bool:
        if directed:
            return edge in self.edges
        return edge in self.edges or tuple(reversed(edge)) in self.edges

    def __contains__(self, other: object) -> bool:
        if isinstance(other, int):
            return other in self._graph
        return False

    @property
    def layout(self) -> dict[Vertex, Position] | None:
        return None

    def draw(self, *, figsize: tuple[float, float] | None = None) -> None:
        if self.layout is None:
            layout = nx.spring_layout(self._graph)
        else:
            layout = self.layout
        if figsize is not None:
            plt.figure(figsize=figsize)

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

        plt.axis("equal")
        plt.show()
