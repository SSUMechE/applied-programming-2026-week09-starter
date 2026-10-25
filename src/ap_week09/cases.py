"""Supplied seven-node teaching input and larger Assignment graph cases."""

GRAPH = {
    "S": ("A", "B"),
    "A": ("S", "C"),
    "B": ("S", "G"),
    "C": ("A", "D"),
    "D": ("C", "G"),
    "G": ("B", "D"),
    "X": (),
}

PARENT_EXAMPLE = {"S": None, "B": "S", "G": "B"}

# The same three algorithms apply to this larger input without special cases.
ASSIGNMENT_GRAPH = {
    "S": ("A", "B"),
    "A": ("S", "H", "E"),
    "B": ("S", "J", "G"),
    "C": ("E", "K", "F"),
    "D": ("F", "L", "G"),
    "E": ("A", "C", "I"),
    "F": ("C", "D", "I"),
    "G": ("B", "D"),
    "H": ("A",),
    "I": ("E", "F"),
    "J": ("B",),
    "K": ("C",),
    "L": ("D",),
    "X": (),
}


def graph_cases() -> dict[str, dict[str, tuple[str, ...]]]:
    """Return fresh dictionaries, preserving the original ordered tuples."""
    original = GRAPH.copy()
    reversed_start = GRAPH.copy()
    reversed_start["S"] = ("B", "A")
    closed_shortcut = GRAPH.copy()
    closed_shortcut["B"] = ("S",)
    closed_shortcut["G"] = ("D",)
    isolated_goal = closed_shortcut.copy()
    isolated_goal["D"] = ("C",)
    isolated_goal["G"] = ()
    return {
        "original": original,
        "reversed_start": reversed_start,
        "closed_shortcut": closed_shortcut,
        "isolated_goal": isolated_goal,
    }


def assignment_cases() -> dict[str, dict[str, tuple[str, ...]]]:
    """Return fresh larger cases, preserving each remaining neighbor's order."""
    original = ASSIGNMENT_GRAPH.copy()
    reversed_start = ASSIGNMENT_GRAPH.copy()
    reversed_start["S"] = ("B", "A")
    closed_shortcut = ASSIGNMENT_GRAPH.copy()
    closed_shortcut["B"] = ("S", "J")
    closed_shortcut["G"] = ("D",)
    isolated_goal = closed_shortcut.copy()
    isolated_goal["D"] = ("F", "L")
    isolated_goal["G"] = ()
    return {
        "original": original,
        "reversed_start": reversed_start,
        "closed_shortcut": closed_shortcut,
        "isolated_goal": isolated_goal,
    }
