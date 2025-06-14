from graphs.utils import Vertex


def path_1(n_vertices: int) -> list[Vertex]:
    return [
        i // 2 if i % 2 == 0 else n_vertices - (i + 1) // 2 for i in range(n_vertices)
    ]


def fork_1(n_vertices: int) -> list[Vertex]:
    return list(reversed(path_1(n_vertices - 2))) + [n_vertices - 2, n_vertices - 1]
