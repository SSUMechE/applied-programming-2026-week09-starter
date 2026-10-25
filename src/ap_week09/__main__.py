"""Run the original graph after all three TODOs are complete."""

from .cases import GRAPH
from .workflow import print_result


def main():
    for method in ("bfs", "dfs"):
        print_result(GRAPH, "S", "G", method)


if __name__ == "__main__":
    main()
