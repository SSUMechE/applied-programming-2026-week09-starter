"""Complete supplied connections between traversal, reconstruction and output."""

from .traversal import bfs, dfs, reconstruct_path
from .validation import validate_graph


def solve(graph, start, goal, method):
    """Validate goal membership, then return (order, parent, path)."""
    validate_graph(graph, start, goal)
    if method == "bfs":
        order, parent = bfs(graph, start)
    elif method == "dfs":
        order, parent = dfs(graph, start)
    else:
        raise ValueError("method must be bfs or dfs")
    path = reconstruct_path(parent, start, goal)
    return order, parent, path


def print_result(graph, start, goal, method):
    order, parent, path = solve(graph, start, goal, method)
    print(method.upper())
    print("order:", order)
    print("parent:", parent)
    print("path:", path)
    print("edges:", None if path is None else len(path) - 1)
