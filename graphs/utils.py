from collections.abc import Sequence
from itertools import chain


Vertex = int
Edge = tuple[Vertex, Vertex]
Position = tuple[float, float]


def subdivide(
    edges: Sequence[Edge], n_subdivisions: int = 1, *, numeric_vertices: bool = True
) -> list[Edge]:
    n_vertices = len(set(chain.from_iterable(edges)))
    new_edges: list[Edge] = []
    if numeric_vertices:
        new_vertex = n_vertices
        for u, v in edges:
            new_edges.extend(
                [(u, new_vertex)]
                + [
                    (new_vertex + i, new_vertex + i + 1)
                    for i in range(n_subdivisions - 1)
                ]
                + [(new_vertex + n_subdivisions - 1, v)]
            )
            new_vertex += n_subdivisions
    return new_edges
