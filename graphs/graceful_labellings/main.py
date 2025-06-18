from collections.abc import Generator
import networkx as nx

from ..utils import Vertex


def find_graceful_labellings(graph: nx.Graph) -> Generator[nx.Graph, None, None]:
    n_edges = len(graph.edges)
    vertex_order = list(graph.nodes)

    valid_vertex_labels = range(n_edges + 1)

    def recurse(
        vertex_labels: dict[Vertex, int] = {}, edge_labels: set[int] = set()
    ) -> Generator[nx.Graph, None, None]:
        if len(edge_labels) == n_edges:
            graceful_graph = graph.copy()
            nx.set_node_attributes(graceful_graph, vertex_labels, name="label")
            yield graceful_graph
            return
        other_labels = [
            label
            for label in valid_vertex_labels
            if label not in vertex_labels.values()
        ]
        new_vertex = vertex_order[len(vertex_labels)]
        neighbors = graph.neighbors(new_vertex)
        labelled_neighbors = list(filter(lambda v: v in vertex_labels, neighbors))
        for label in other_labels:
            new_edge_labels = {
                abs(label - vertex_labels[v]) for v in labelled_neighbors
            }
            if (
                len(new_edge_labels) == len(labelled_neighbors)
                and len(new_edge_labels & edge_labels) == 0
            ):
                yield from recurse(
                    vertex_labels | {new_vertex: label},
                    edge_labels | new_edge_labels,
                )

    yield from recurse()
