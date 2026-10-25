"""Complete supplied stage runner. Students edit traversal.py, not this file."""

import argparse

from ap_week09.cases import GRAPH, PARENT_EXAMPLE, assignment_cases
from ap_week09.traversal import bfs, dfs, reconstruct_path
from ap_week09.workflow import print_result


def main():
    parser = argparse.ArgumentParser(description="Inspect the Week 9 traversal results")
    parser.add_argument("--stage", choices=("reconstruct", "bfs", "dfs"))
    arguments = parser.parse_args()
    if arguments.stage == "reconstruct":
        for goal in ("G", "S", "X"):
            path = reconstruct_path(PARENT_EXAMPLE, "S", goal)
            print(f"S -> {goal}:", path)
        return
    if arguments.stage in ("bfs", "dfs"):
        traversal = bfs if arguments.stage == "bfs" else dfs
        order, parent = traversal(GRAPH, "S")
        print("order:", order)
        print("parent:", parent)
        return
    for case_name, graph in assignment_cases().items():
        print(f"[{case_name}]")
        for method in ("bfs", "dfs"):
            print_result(graph, "S", "G", method)


if __name__ == "__main__":
    main()
