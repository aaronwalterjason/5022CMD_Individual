"""A generic unweighted directed graph, stored as two adjacency lists."""
from collections import deque


class DirectedGraph:
    """Generic unweighted directed graph. Vertices can be any hashable object."""

    def __init__(self):
        self._outgoing = {}  # Vertex -> vertices it points to
        self._incoming = {}  # Vertex -> vertices pointing to it

    # ==================================================================
    # Vertices
    # ==================================================================
    def add_vertex(self, vertex):
        """Add a new vertex. Return False if it already exists. O(1)."""
        if vertex in self._outgoing:
            return False
        self._outgoing[vertex] = []
        self._incoming[vertex] = []
        return True

    def has_vertex(self, vertex):
        """Return True if the vertex is in the graph. O(1)."""
        return vertex in self._outgoing

    def vertices(self):
        """Return all vertices in the order they were added. O(V)."""
        return list(self._outgoing)

    # ==================================================================
    # Edges
    # ==================================================================
    def add_edge(self, from_vertex, to_vertex):
        """Connect from_vertex -> to_vertex.

        Return False if either vertex is missing or the edge already exists.
        """
        if not self.has_vertex(from_vertex) or not self.has_vertex(to_vertex):
            return False
        if self.has_edge(from_vertex, to_vertex):
            return False
        # Both lists are updated so either direction can be looked up straight away
        self._outgoing[from_vertex].append(to_vertex)
        self._incoming[to_vertex].append(from_vertex)
        return True

    def remove_edge(self, from_vertex, to_vertex):
        """Remove the edge from_vertex -> to_vertex. Return False if there was no such edge."""
        if not self.has_edge(from_vertex, to_vertex):
            return False
        self._outgoing[from_vertex].remove(to_vertex)
        self._incoming[to_vertex].remove(from_vertex)
        return True

    def has_edge(self, from_vertex, to_vertex):
        """Return True if from_vertex has an edge going to to_vertex."""
        return self.has_vertex(from_vertex) and to_vertex in self._outgoing[from_vertex]

    # ==================================================================
    # Neighbours
    # ==================================================================
    def list_incoming_adjacent_vertex(self, vertex):
        """Return every vertex with an edge coming into this vertex. O(in-degree)."""
        return list(self._incoming.get(vertex, []))

    def list_outgoing_adjacent_vertex(self, vertex):
        """Return every vertex this vertex has an edge going to. O(out-degree)."""
        return list(self._outgoing.get(vertex, []))

    # ==================================================================
    # Traversal
    # ==================================================================
    def has_path(self, start, goal):
        """Return True if goal can be reached from start by following edges (BFS). O(V + E)."""
        if not self.has_vertex(start) or not self.has_vertex(goal):
            return False
        if start == goal:
            return True
        visited = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour in self._outgoing[current]:
                if neighbour == goal:
                    return True
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return False

    def topological_levels(self):
        """Group vertices into levels, so every edge comes from an earlier level.

        Return a list of lists, or None if there is a cycle.
        """
        waiting = {vertex: len(self._incoming[vertex]) for vertex in self._outgoing}
        current_level = [vertex for vertex in self._outgoing if waiting[vertex] == 0]
        levels = []
        while current_level:
            levels.append(current_level)
            next_level = []
            # Finishing this level frees up the vertices whose last incoming edge came from it
            for vertex in current_level:
                for neighbour in self._outgoing[vertex]:
                    waiting[neighbour] -= 1
                    if waiting[neighbour] == 0:
                        next_level.append(neighbour)
            current_level = next_level
        placed = sum(len(level) for level in levels)
        return levels if placed == len(self._outgoing) else None

    def __len__(self):
        """Return how many vertices are in the graph."""
        return len(self._outgoing)