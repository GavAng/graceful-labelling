from collections.abc import Mapping
import matplotlib.pyplot as plt
import networkx as nx

from ..utils import Vertex


def draw_labelled_graph(
    graph: nx.Graph,
    *,
    layout: Mapping[Vertex, int] | None = None,
    figsize: tuple[float, float] | None = None,
) -> None:
    """
    Assumes graph has integer attribute "label".
    """
    if layout is None:
        layout = nx.spring_layout(graph)
    if figsize is not None:
        plt.figure(figsize=figsize)

    nx.draw(
        graph,
        pos=layout,
        with_labels=False,
        node_color="lightblue",
    )

    vertex_labels = nx.get_node_attributes(graph, "label")
    nx.draw_networkx_labels(graph, pos=layout, labels=vertex_labels, font_size=12)

    edge_labels = {
        (u, v): abs(vertex_labels[u] - vertex_labels[v]) for u, v in graph.edges
    }
    nx.draw_networkx_edge_labels(
        graph,
        pos=layout,
        edge_labels=edge_labels,
    )

    plt.axis("equal")
    plt.show()
