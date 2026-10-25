"""Supplied checks for TODO 2. Run them unchanged."""

from ap_week09.cases import ASSIGNMENT_GRAPH, assignment_cases
from ap_week09.traversal import bfs


def test_bfs_original_cycle():
    """FIFO reaches every branch once and discovers G from B, with X unreachable."""
    graph = ASSIGNMENT_GRAPH.copy()
    before = graph.copy()
    order, parent = bfs(graph, "S")
    assert order == ["S", "A", "B", "H", "E", "J", "G", "C", "I", "D", "K", "F", "L"]
    assert parent == {
        "S": None, "A": "S", "B": "S", "H": "A", "E": "A", "J": "B",
        "G": "B", "C": "E", "I": "E", "D": "G", "K": "C", "F": "C", "L": "D",
    }
    assert graph == before


def test_bfs_isolated_start():
    """Starting at isolated X processes X and records only its root parent."""
    assert bfs(ASSIGNMENT_GRAPH, "X") == (["X"], {"X": None})


def test_bfs_neighbor_order():
    """Reversing only S's neighbors lets D discover F before C does."""
    order, parent = bfs(assignment_cases()["reversed_start"], "S")
    assert order == ["S", "B", "A", "J", "G", "H", "E", "D", "C", "I", "F", "L", "K"]
    assert parent["F"] == "D"
