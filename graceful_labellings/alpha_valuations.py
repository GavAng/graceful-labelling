from collections.abc import Sequence

from graphs.fork_graph import ForkGraphArgs
from graphs.path_graph import PathGraph
from graphs.utils import Vertex


def path_1(n_vertices: int) -> Sequence[Vertex]:
    return [
        i // 2 if i % 2 == 0 else n_vertices - (i + 1) // 2 for i in range(n_vertices)
    ]


def fork_1(n_vertices: int) -> ForkGraphArgs:
    return {
        "path": PathGraph.from_vertices_standard(path_1(n_vertices - 2)),
        "ends": ((0, n_vertices - 2), (0, n_vertices - 1)),
    }
