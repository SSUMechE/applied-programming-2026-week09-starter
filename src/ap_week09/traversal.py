"""Complete only the three marked algorithm regions. Keep supplied code intact."""

from collections import deque

from .validation import validate_graph, validate_parent


def reconstruct_path(
    parent: dict[str, str | None], start: str, goal: str
) -> list[str] | None:
    """Return a new start-to-goal list, or None when goal is absent from parent.

    parent, start and goal are supplied arguments. Read the existing parent
    mapping. Do not construct it or run BFS/DFS here. In this input,
    parent[start] is None and each other key maps to its predecessor.
    The supplied check rejects malformed parent mappings.

    Create a new path list by following predecessors from goal. Return the
    list in start-to-goal order. Preserve parent. Return [start] when start
    equals goal, or None when goal is absent from parent. Do not print.
    """
    validate_parent(parent, start, goal)
    # BEGIN TODO 1: reconstruct_path
    raise NotImplementedError("Complete TODO 1: reconstruct_path")
    # END TODO 1


def bfs(
    graph: dict[str, tuple[str, ...]], start: str
) -> tuple[list[str], dict[str, str | None]]:
    """Return (order, parent) for all nodes reachable from start using BFS.

    graph and start are supplied arguments. graph maps node IDs to ordered
    neighbor tuples. Create a local queue, visited set, order list and parent
    dictionary. Here parent is a new output mapping, not a supplied argument.

    Use a deque as a FIFO queue. Mark a node visited and assign its parent on
    first enqueue. Inspect neighbors in tuple order. In the returned mapping,
    parent[start] is None. order records actual processing order. Return the
    new (order, parent) collections. Preserve graph. Do not stop at a goal or print.
    """
    validate_graph(graph, start)
    # BEGIN TODO 2: bfs
    raise NotImplementedError("Complete TODO 2: bfs")
    # END TODO 2


def dfs(
    graph: dict[str, tuple[str, ...]], start: str
) -> tuple[list[str], dict[str, str | None]]:
    """Return (order, parent) for all nodes reachable from start using DFS.

    graph and start are supplied arguments. graph maps node IDs to ordered
    neighbor tuples. Create a local stack, visited set, order list and parent
    dictionary. Here parent is a new output mapping, not a supplied argument.

    Use a deque as a LIFO stack of (node, parent_candidate) pairs, initially
    (start, None). Finalize visited and parent on the first pop of each node.
    Skip a node already visited. Push currently unvisited neighbors in reversed
    tuple order. A pending stack entry is not a visited node. Preserve the first
    finalized parent. In the returned mapping, parent[start] is None. order
    records first-pop processing order. Return the new (order, parent)
    collections. Preserve graph. Do not stop at a goal or print.
    """
    validate_graph(graph, start)
    # BEGIN TODO 3: dfs
    raise NotImplementedError("Complete TODO 3: dfs")
    # END TODO 3
