"""Complete supplied input checks. These are not student implementation tasks."""


def _node_id(value: object, label: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a nonempty string")


def validate_graph(graph: object, start: str, goal: str | None = None) -> None:
    """Accept directed adjacency dictionaries with ordered unique neighbors.

    An undirected edge is represented by both directed entries. A self-loop is
    allowed. Duplicate neighbors and references to missing keys are rejected.
    goal is checked only when supplied by a caller that has the full graph.
    """
    if not isinstance(graph, dict) or not graph:
        raise ValueError("graph must be a nonempty dictionary")
    for node in graph:
        _node_id(node, "node ID")
    for node, neighbors in graph.items():
        if not isinstance(neighbors, tuple):
            raise ValueError(f"neighbors of {node} must be a tuple")
        seen = set()
        for neighbor in neighbors:
            _node_id(neighbor, "neighbor ID")
            if neighbor not in graph:
                raise ValueError(f"neighbor {neighbor} of {node} is missing from graph")
            if neighbor in seen:
                raise ValueError(f"duplicate neighbor {neighbor} of {node}")
            seen.add(neighbor)
    _node_id(start, "start")
    if start not in graph:
        raise ValueError("start is missing from graph")
    if goal is not None:
        _node_id(goal, "goal")
        if goal not in graph:
            raise ValueError("goal is missing from graph")


def validate_parent(parent: object, start: str, goal: str) -> None:
    """Check a single rooted parent mapping without changing it.

    This mapping contains reached nodes only. It cannot determine whether an
    absent goal exists in a separate graph. The supplied workflow checks that.
    """
    _node_id(start, "start")
    _node_id(goal, "goal")
    if not isinstance(parent, dict) or not parent:
        raise ValueError("parent must be a nonempty dictionary")
    for node in parent:
        _node_id(node, "parent key")
    if start not in parent or parent[start] is not None:
        raise ValueError("parent[start] must be None")
    for node, previous in parent.items():
        if node == start:
            continue
        _node_id(previous, "parent value")
        if previous not in parent:
            raise ValueError(f"parent of {node} is missing from mapping")
    checked = {start}
    for node in parent:
        chain = set()
        current = node
        while current not in checked:
            if current in chain:
                raise ValueError("parent mapping contains a cycle")
            chain.add(current)
            current = parent[current]
        checked.update(chain)
