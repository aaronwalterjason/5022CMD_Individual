"""Quick checks that the graph works on its own, using text and number vertices."""
from graph import DirectedGraph

g = DirectedGraph()  # Plain text vertices show the graph doesn't depend on Course

print("=== Add vertices ===")
for v in ["A", "B", "C", "D"]:
    print(v, "->", g.add_vertex(v))
print("Duplicate A ->", g.add_vertex("A"))

print("\n=== Add edges ===")
print("A -> C :", g.add_edge("A", "C"))
print("B -> C :", g.add_edge("B", "C"))
print("C -> D :", g.add_edge("C", "D"))
print("Duplicate A -> C :", g.add_edge("A", "C"))
print("Missing vertex A -> Z :", g.add_edge("A", "Z"))

print("\n=== Incoming / outgoing ===")
print("Incoming C :", g.list_incoming_adjacent_vertex("C"))
print("Outgoing C :", g.list_outgoing_adjacent_vertex("C"))
print("Incoming A :", g.list_incoming_adjacent_vertex("A"))

print("\n=== Path and study order ===")
print("Path A -> D :", g.has_path("A", "D"))
print("Path D -> A :", g.has_path("D", "A"))
print("Topological levels:", g.topological_levels())
g.add_edge("D", "A")  # Creates a loop A -> C -> D -> A
print("Levels with a loop:", g.topological_levels())
g.remove_edge("D", "A")

print("\n=== Remove ===")
print("Remove edge B -> C :", g.remove_edge("B", "C"))
print("Incoming C :", g.list_incoming_adjacent_vertex("C"))
print("Outgoing B :", g.list_outgoing_adjacent_vertex("B"))
print("Vertices :", g.vertices())

print("\n=== Works with numbers too ===")
n = DirectedGraph()
n.add_vertex(1)
n.add_vertex(2)
n.add_edge(1, 2)
print("Incoming 2 :", n.list_incoming_adjacent_vertex(2))