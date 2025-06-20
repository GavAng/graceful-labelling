from collections.abc import Generator
import networkx as nx

from ..utils import Edge, Vertex


def find_graceful_labellings(graph: nx.Graph) -> Generator[nx.Graph, None, None]:
    n_edges = len(graph.edges)
    vertex_order = list(graph.nodes)

    valid_vertex_labels = range(n_edges + 1)

    def recurse(
        vertex_labels: dict[Vertex, int] = {}, edge_labels: dict[Edge, int] = {}
    ) -> Generator[nx.Graph, None, None]:
        if len(edge_labels) == n_edges:
            graceful_graph = graph.copy()
            nx.set_node_attributes(graceful_graph, vertex_labels, name="label")
            nx.set_edge_attributes(graceful_graph, edge_labels, name="label")

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
                (new_vertex, v): abs(label - vertex_labels[v])
                for v in labelled_neighbors
            }
            if (
                len(set(new_edge_labels.values())) == len(labelled_neighbors)
                and set(new_edge_labels.values()) & set(edge_labels.values()) == set()
            ):
                yield from recurse(
                    vertex_labels | {new_vertex: label},
                    edge_labels | new_edge_labels,
                )

    yield from recurse()


def find_alpha_valuations(graph: nx.Graph) -> Generator[nx.Graph, None, None]:
    # every alpha valuation is a graceful labelling (by definition)
    for graceful_graph in find_graceful_labellings(graph):
        vertex_labels = nx.get_node_attributes(graceful_graph, "label")
        edge_labels = nx.get_edge_attributes(graceful_graph, "label")
        # existence and uniqueness means we can do this:
        u, v = list(filter(lambda edge: edge_labels[edge] == 1, edge_labels))[0]
        # x as defined in the definition of alpha valuations:
        x = min(vertex_labels[u], vertex_labels[v])
        is_alpha_valuation = True
        for u, v in graph.edges:
            if (vertex_labels[u] <= x and vertex_labels[v] <= x) or (
                vertex_labels[u] > x and vertex_labels[v] > x
            ):
                is_alpha_valuation = False
                break
        if is_alpha_valuation:
            yield graceful_graph
