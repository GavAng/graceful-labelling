from itertools import pairwise
from .utils import Edge


def path(n_vertices: int) -> list[Edge]:
    if n_vertices <= 0:
        raise ValueError("Path graph must be of size at least 1.")
    return list(pairwise(range(n_vertices)))


def cycle(n_vertices: int) -> list[Edge]:
    if n_vertices <= 2:
        raise ValueError("Cyclic graph must be of size at least 3.")
    return path(n_vertices) + [(n_vertices - 1, 0)]
