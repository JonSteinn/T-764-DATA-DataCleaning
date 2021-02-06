from collections import defaultdict
from typing import DefaultDict, Iterator, Set


class Graph:
    """A non-directed graph."""

    def __init__(self):
        self.edges: DefaultDict[int, Set[int]] = defaultdict(set)

    def add_edge(self, vertex1: int, vertex2: int):
        """Connect two vertices."""
        self.edges[vertex1].add(vertex2)
        self.edges[vertex2].add(vertex1)

    def find_grps(self) -> Iterator[Set[int]]:
        """Yields all connected componenets. Note that this consumes the graph
        object.
        """
        while self.edges:
            stack = [next(iter(self.edges), -1)]
            visited = {stack[0]}
            while stack:
                curr = stack.pop()
                for neighbor in self.edges.pop(curr):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            yield visited
