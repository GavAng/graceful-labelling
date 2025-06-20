import base64
from collections.abc import Iterable, Mapping
from IPython.display import display, HTML
import io
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import networkx as nx
import uuid

from ..utils import Position, Vertex


def labelled_graph_to_axis(
    graph: nx.Graph,
    *,
    ax: Axes | None = None,
    layout: Mapping[Vertex, Position],
) -> Axes:
    if ax is None:
        _, ax = plt.subplots()

    nx.draw(
        graph,
        pos=layout,
        ax=ax,
        with_labels=False,
        node_color="lightblue",
    )

    vertex_labels = nx.get_node_attributes(graph, "label")
    nx.draw_networkx_labels(graph, pos=layout, ax=ax, labels=vertex_labels)

    edge_labels = nx.get_edge_attributes(graph, "label")
    nx.draw_networkx_edge_labels(
        graph,
        pos=layout,
        ax=ax,
        edge_labels=edge_labels,
    )

    return ax


def draw_labelled_graph(
    graph: nx.Graph,
    *,
    layout: Mapping[Vertex, Position] | None = None,
    figsize: tuple[float, float] | None = None,
) -> None:
    """
    Assumes graph has integer attribute "label".
    """
    if layout is None:
        layout = nx.spring_layout(graph)
    if figsize is not None:
        plt.figure(figsize=figsize)
    ax = labelled_graph_to_axis(graph, layout=layout)
    plt.axis("equal")
    plt.show()


def draw_slideshow(
    graphs: Iterable[nx.Graph], *, layout: Mapping[Vertex, Position] | None = None
) -> None:
    graph_drawings: list[str] = []
    for graph in graphs:
        if layout is None:
            layout = nx.spring_layout(graph)

        fig, ax = plt.subplots()
        ax = labelled_graph_to_axis(graph, ax=ax, layout=layout)

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)

        img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        graph_drawings.append(img_base64)

    unique_id = f"slideshow_{uuid.uuid4().hex}"

    html = f"""
    <div id="{unique_id}-container" style="max-width:600px; text-align:center;">
        <img id="{unique_id}-img" src="data:image/png;base64,{graph_drawings[0]}" style="width:100%; max-height:500px;"/>
        <div style="margin: 8px 0;">
            <span id="{unique_id}-counter">1 / {len(graph_drawings)}</span>
        </div>
        <button id="{unique_id}-prev">Previous</button>
        <button id="{unique_id}-next">Next</button>
    </div>
    <script>
        (function() {{
            let images = [{",".join(f'"{graph}"' for graph in graph_drawings)}];
            let index = 0;
            const total = images.length;

            function showImage(i) {{
                document.getElementById("{unique_id}-img").src = "data:image/png;base64," + images[i];
                document.getElementById("{unique_id}-counter").textContent = (i + 1) + " / " + total;
            }}

            document.getElementById("{unique_id}-prev").onclick = function() {{
                index = (index - 1 + images.length) % images.length;
                showImage(index);
            }};
            document.getElementById("{unique_id}-next").onclick = function() {{
                index = (index + 1) % images.length;
                showImage(index);
            }};
        }})();
    </script>
    """

    display(HTML(html))
