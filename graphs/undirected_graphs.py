from abc import ABC, abstractmethod
from itertools import pairwise
import math
from typing import override

from .utils import Edge, Position, Vertex


class UndirectedGraph(ABC):
    @staticmethod
    @abstractmethod
    def edges(n_vertices: int) -> list[Edge]: ...

    @staticmethod
    @abstractmethod
    def layout(n_vertices: int) -> dict[Vertex, Position]: ...


class PathGraph(UndirectedGraph):
    @override
    @staticmethod
    def edges(n_vertices: int) -> list[Edge]:
        if n_vertices <= 0:
            raise ValueError("Path graph must be of size at least 1.")
        return list(pairwise(range(n_vertices)))

    @override
    @staticmethod
    def layout(n_vertices: int) -> dict[Vertex, Position]:
        return {i: (i, 0) for i in range(n_vertices)}


class CycleGraph(UndirectedGraph):
    @override
    @staticmethod
    def edges(n_vertices: int) -> list[Edge]:
        if n_vertices <= 2:
            raise ValueError("Cyclic graph must be of size at least 3.")
        return PathGraph.edges(n_vertices) + [(n_vertices - 1, 0)]

    @override
    @staticmethod
    def layout(n_vertices: int) -> dict[Vertex, Position]:
        angle = 2 * math.pi / n_vertices
        if n_vertices % 4 == 0:
            layout = {
                i: (math.cos((i + 0.5) * angle), math.sin((i + 0.5) * angle))
                for i in range(n_vertices)
            }
        else:
            layout = {
                i: (math.sin(i * angle), math.cos(i * angle)) for i in range(n_vertices)
            }
        return layout


class CompleteGraph(UndirectedGraph):
    @override
    @staticmethod
    def edges(n_vertices: Vertex) -> list[Edge]:
        return [(i, j) for i in range(n_vertices) for j in range(i + 1, n_vertices)]

    @override
    @staticmethod
    def layout(n_vertices: Vertex) -> dict[Vertex, Position]:
        return CycleGraph.layout(n_vertices)


class StarGraph(UndirectedGraph):
    @override
    @staticmethod
    def edges(n_vertices: Vertex) -> list[Edge]:
        return [(n_vertices, i) for i in range(n_vertices)]

    @override
    @staticmethod
    def layout(n_vertices: Vertex) -> dict[Vertex, Position]:
        return CycleGraph.layout(n_vertices) | {n_vertices: (0, 0)}


class SunGraph(UndirectedGraph):
    @override
    @staticmethod
    def edges(n_vertices: int) -> list[Edge]:
        return CycleGraph.edges(n_vertices) + [
            (i, i + n_vertices) for i in range(n_vertices)
        ]

    @override
    @staticmethod
    def layout(n_vertices: Vertex) -> dict[Vertex, Position]:
        cycle_layout = CycleGraph.layout(n_vertices)
        return cycle_layout | {
            i + n_vertices: (2 * x, 2 * y) for i, (x, y) in cycle_layout.items()
        }


class WheelGraph(UndirectedGraph):
    @override
    @staticmethod
    def edges(n_vertices: int) -> list[Edge]:
        return CycleGraph.edges(n_vertices - 1) + StarGraph.edges(n_vertices - 1)

    @override
    @staticmethod
    def layout(n_vertices: Vertex) -> dict[Vertex, Position]:
        return StarGraph.layout(n_vertices - 1)
