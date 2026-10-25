"""Supplied checks for TODO 1. Run them unchanged."""

from ap_week09.traversal import reconstruct_path


def test_reconstruct_start_to_goal():
    """G -> B -> S in parent becomes a new S-to-G list without changing parent."""
    parent = {"S": None, "B": "S", "G": "B"}
    before = parent.copy()
    assert reconstruct_path(parent, "S", "G") == ["S", "B", "G"]
    assert parent == before


def test_reconstruct_already_at_goal():
    """A zero-edge route contains the start once, not an empty list."""
    assert reconstruct_path({"S": None}, "S", "S") == ["S"]


def test_reconstruct_unreachable_goal():
    """X is absent from the reached-node parent mapping, so the result is None."""
    assert reconstruct_path({"S": None, "B": "S"}, "S", "X") is None
