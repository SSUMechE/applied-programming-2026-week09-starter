"""Complete supplied example. This runs before all three Assignment TODOs."""

from ap_week09.cases import GRAPH, PARENT_EXAMPLE
from ap_week09.validation import validate_graph, validate_parent

validate_graph(GRAPH, "S", "G")
validate_parent(PARENT_EXAMPLE, "S", "G")
print("neighbors of S:", GRAPH["S"])
print("neighbors of X:", GRAPH["X"])
print("node count:", len(GRAPH))
print("undirected edge count:", sum(len(neighbors) for neighbors in GRAPH.values()) // 2)
print("supplied parent mapping:", PARENT_EXAMPLE)
print("parent of G:", PARENT_EXAMPLE["G"])
print("parent of B:", PARENT_EXAMPLE["B"])
print("parent of S:", PARENT_EXAMPLE["S"])
