"""Supplied checks for TODO 3. Run them unchanged."""

from ap_week09.cases import ASSIGNMENT_GRAPH, assignment_cases
from ap_week09.traversal import dfs


def test_dfs_original_cycle():
    """B and I retain their first popped parents despite earlier pending pairs."""
    graph = ASSIGNMENT_GRAPH.copy()
    before = graph.copy()
    order, parent = dfs(graph, "S")
    assert order == ["S", "A", "H", "E", "C", "K", "F", "D", "L", "G", "B", "J", "I"]
    assert parent == {
        "S": None, "A": "S", "H": "A", "E": "A", "C": "E", "K": "C",
        "F": "C", "D": "F", "L": "D", "G": "D", "B": "G", "J": "B", "I": "F",
    }
    assert graph == before


def test_dfs_isolated_start():
    """Starting at isolated X processes X and records only its root parent."""
    assert dfs(ASSIGNMENT_GRAPH, "X") == (["X"], {"X": None})


def test_dfs_neighbor_order():
    """A pending A candidate does not prevent reaching A through the B branch."""
    order, parent = dfs(assignment_cases()["reversed_start"], "S")
    assert order == ["S", "B", "J", "G", "D", "F", "C", "E", "A", "H", "I", "K", "L"]
    assert parent["G"] == "B"
    assert parent["A"] == "E"
